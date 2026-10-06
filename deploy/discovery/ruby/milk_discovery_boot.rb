# frozen_string_literal: true
require "milk_discovery"
if MilkDiscovery.enabled?
  MilkDiscovery.wait_for(*ENV.fetch("DISCOVERY_DEPENDENCIES", "").split(",").reject(&:empty?))
  require "sequel"
  Sequel::Database.prepend(MilkDiscovery::DatabaseRouting)
  MilkDiscovery.start_registration! unless ENV["DISCOVERY_COMMAND"] == "1"
end
