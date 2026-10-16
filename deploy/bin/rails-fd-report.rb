# frozen_string_literal: true

# Run inside a Rails container: compose.sh exec -T schedule_web ruby < this_file
# Report descriptors owned by each Ruby process, never credentials or arguments.
require "json"

states = { "01" => "established", "02" => "syn_sent", "03" => "syn_recv",
           "04" => "fin_wait1", "05" => "fin_wait2", "06" => "time_wait",
           "07" => "closed", "08" => "close_wait", "09" => "last_ack",
           "0A" => "listen", "0B" => "closing" }

Dir.glob("/proc/[0-9]*").sort.each do |path|
  begin
    pid = File.basename(path).to_i
    next if pid == Process.pid
    next unless File.read("#{path}/comm").strip.match?(/ruby|falcon/)

    sockets = {}
    %w[tcp tcp6 udp udp6].each do |protocol|
      table = "#{path}/net/#{protocol}"
      next unless File.readable?(table)
      File.readlines(table).drop(1).each do |row|
        fields = row.split
        remote_port = fields[2].split(":").last.to_i(16)
        state = protocol.start_with?("tcp") ? states.fetch(fields[3], fields[3]) : fields[3]
        sockets[fields[9]] = "#{protocol}:#{state}:remote_port=#{remote_port}"
      end
    end

    descriptors = Dir.children("#{path}/fd")
    categories = Hash.new(0)
    descriptors.each do |fd|
      begin
        target = File.readlink("#{path}/fd/#{fd}")
        inode = target[/\Asocket:\[(\d+)\]\z/, 1]
        category = if inode
          sockets.fetch(inode, "socket:other")
        elsif target.start_with?("anon_inode:")
          target
        elsif target.start_with?("pipe:")
          "pipe"
        else
          "file_or_device"
        end
        categories[category] += 1
      rescue SystemCallError
        # The worker may close a descriptor during inspection.
      end
    end
    limits = File.readlines("#{path}/limits").find { |line| line.start_with?("Max open files") }.split
    soft = limits[3] == "unlimited" ? nil : limits[3].to_i
    puts JSON.generate(pid: pid, descriptors: descriptors.size, soft_limit: soft,
                       utilization: soft && (descriptors.size.to_f / soft).round(4),
                       categories: categories.sort.to_h)
  rescue SystemCallError
    # A worker can exit while /proc is being inspected.
  end
end
