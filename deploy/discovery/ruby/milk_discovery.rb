# frozen_string_literal: true
require "json"
require "net/http"
require "uri"
require "ipaddr"
require "socket"
require "thread"

module MilkDiscovery
  class Unavailable < StandardError; end
  @cache = {}
  @lock = Mutex.new

  def self.enabled? = ENV["DISCOVERY_ENABLED"] == "1"
  def self.clock = Process.clock_gettime(Process::CLOCK_MONOTONIC)

  def self.request(path, payload: nil, method: :get)
    uri = URI(ENV.fetch("CONSUL_HTTP_ADDR") + path)
    http = Net::HTTP.new(uri.host, uri.port, nil)
    http.open_timeout = 1
    http.read_timeout = 2
    req = (method == :put ? Net::HTTP::Put : Net::HTTP::Get).new(uri.request_uri)
    req["X-Consul-Token"] = File.read(ENV.fetch("CONSUL_TOKEN_FILE")).strip
    req["Content-Type"] = "application/json"
    req.body = JSON.generate(payload) if payload
    response = http.request(req)
    raise Unavailable, "Discovery request rejected" unless response.is_a?(Net::HTTPSuccess)
    response.body.to_s.empty? ? nil : JSON.parse(response.body)
  end

  def self.instances(service)
    now = clock
    cached = @lock.synchronize { @cache[service] }
    if cached && now - cached[0] < 5
      raise Unavailable, "No healthy #{service} instance" if cached[1].empty?
      return cached[1]
    end
    begin
      rows = request("/v1/health/service/#{URI.encode_www_form_component(service)}?passing=true")
      found = rows.map do |row|
        entry = row.fetch("Service")
        ip = IPAddr.new(entry.fetch("Address")).to_s
        port = Integer(entry.fetch("Port"))
        raise Unavailable, "Invalid discovered port" unless (1..65_535).cover?(port)
        [ip, port]
      end.uniq.sort
    rescue StandardError
      return cached[1] if cached && !cached[1].empty? && now - cached[0] < 60
      raise Unavailable, "Discovery unavailable for #{service}"
    end
    @lock.synchronize { @cache[service] = [clock, found] }
    raise Unavailable, "No healthy #{service} instance" if found.empty?
    found
  end

  def self.endpoint(service, scheme: "http")
    host, port = instances(service).first
    "#{scheme}://#{host}:#{port}"
  end

  def self.database_url
    return ENV.fetch("DATABASE_URL") unless enabled?
    host, port = instances("postgres").first
    user, password, database = %w[POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB].map do |key|
      URI.encode_www_form_component(ENV.fetch(key)).gsub("+", "%20")
    end
    "postgresql://#{user}:#{password}@#{host}:#{port}/#{database}"
  end

  def self.redis_url
    return ENV.fetch("REDIS_URL") unless enabled?
    host, port = instances("redis").first
    password = URI.encode_www_form_component(ENV.fetch("REDIS_PASSWORD")).gsub("+", "%20")
    "redis://:#{password}@#{host}:#{port}/#{ENV.fetch('REDIS_DB', '0')}"
  end

  def self.minio_url = enabled? ? endpoint("minio") : ENV.fetch("MINIO_ENDPOINT")
  def self.scheduler_url = enabled? ? endpoint("scheduler") : ENV.fetch("SCHEDULER_URL", "http://scheduler:8100")

  def self.wait_for(*services)
    deadline = clock + 120
    services.each do |service|
      loop do
        begin
          instances(service)
          break
        rescue Unavailable
          raise Unavailable, "Discovery startup deadline exceeded" if clock >= deadline
          sleep 2
        end
      end
    end
  end

  def self.heartbeat!
    @heartbeat = clock
  end

  def self.worker_healthy?
    @heartbeat && clock - @heartbeat < Integer(ENV.fetch("WORKER_HEARTBEAT_MAX_AGE", "30"))
  end

  def self.start_registration!
    return unless enabled? && ENV["DISCOVERY_SERVICE"]
    return if @registration_pid == Process.pid
    @registration_pid = Process.pid
    @stop = false
    service = ENV.fetch("DISCOVERY_SERVICE")
    id = "#{service}-#{Socket.gethostname}"
    @registration = Thread.new do
      until @stop
        begin
          target = URI(ENV.fetch("CONSUL_HTTP_ADDR"))
          socket = UDPSocket.new
          socket.connect(target.host, target.port)
          address = socket.addr.last
          socket.close
          port = Integer(ENV.fetch("DISCOVERY_PORT", "0"))
          # Consul probes HTTP services independently of their Ruby VM/thread.
          # TTL remains appropriate for workers, whose progress is measured here.
          check = if ENV["DISCOVERY_HEALTH_PATH"]
            { HTTP: "http://#{address}:#{port}#{ENV.fetch('DISCOVERY_HEALTH_PATH')}",
              Interval: "5s", Timeout: "3s", DeregisterCriticalServiceAfter: "2m" }
          else
            { TTL: "15s", DeregisterCriticalServiceAfter: "2m" }
          end
          request("/v1/agent/service/register?replace-existing-checks=true", method: :put, payload: {
            ID: id, Name: service, Address: address, Port: port,
            Meta: { revision: ENV.fetch("APP_REVISION", "unknown") }, Check: check
          })
          unless ENV["DISCOVERY_HEALTH_PATH"]
            healthy = worker_healthy? && ENV.fetch("DISCOVERY_DEPENDENCIES", "").split(",").all? { |name| !instances(name).empty? }
            request("/v1/agent/check/#{healthy ? 'pass' : 'fail'}/service:#{id}", method: :put)
          end
          registration_error = nil
        rescue StandardError => error
          # Log only the exception class, never response bodies or credentials.
          if registration_error != error.class
            warn "[discovery] Registration failed for #{service}: #{error.class}"
          end
          registration_error = error.class
        end
        sleep 5
      end
    end
    at_exit do
      @stop = true
      @registration&.kill
      begin
        request("/v1/agent/service/deregister/#{id}", method: :put)
      rescue StandardError
        nil
      end
    end
  end

  # Each checkout validates discovery; idle Redis clients reconnect when their endpoint changes.
  class RedisClient
    def initialize(**options)
      require "redis"
      require "connection_pool"
      @pool = ConnectionPool.new(size: Integer(ENV.fetch("REDIS_POOL_SIZE", "7")), timeout: 2) { {} }
      @options = options
    end

    def method_missing(name, *args, **kwargs, &block)
      url = MilkDiscovery.redis_url
      @pool.with do |slot|
        if slot[:url] != url
          slot[:client]&.close
          slot[:client] = ::Redis.new(url: url, timeout: 2, **@options)
          slot[:url] = url
        end
        slot[:client].public_send(name, *args, **kwargs, &block)
      end
    end

    def respond_to_missing?(_name, _private = false) = true
  end

  module DatabaseRouting
    def synchronize(server = nil, &block)
      return super unless MilkDiscovery.enabled? && database_type == :postgres
      host, port = MilkDiscovery.instances("postgres").first
      @milk_discovery_mutex ||= Mutex.new
      @milk_discovery_mutex.synchronize do
        if @milk_discovery_address != [host, port]
          disconnect
          @milk_discovery_address = [host, port]
        end
      end
      super
    end

    def server_opts(server)
      options = super
      return options unless MilkDiscovery.enabled? && database_type == :postgres
      host, port = MilkDiscovery.instances("postgres").first
      options.merge(host: host, port: port)
    end
  end

  # Shrine delegates storage operations to a fresh endpoint-aware instance.
  class Storage
    def initialize(**options)
      @options = options.reject { |key, _| key == :endpoint }
    end

    def url(*args, **kwargs)
      require "shrine/storage/s3"
      Shrine::Storage::S3.new(**@options, endpoint: ENV.fetch("NOTICE_EXPORT_PUBLIC_ENDPOINT")).url(*args, **kwargs)
    end

    def method_missing(name, *args, **kwargs, &block)
      require "shrine/storage/s3"
      storage = Shrine::Storage::S3.new(**@options, endpoint: MilkDiscovery.minio_url)
      storage.public_send(name, *args, **kwargs, &block)
    end

    def respond_to_missing?(_name, _private = false) = true
  end
end
