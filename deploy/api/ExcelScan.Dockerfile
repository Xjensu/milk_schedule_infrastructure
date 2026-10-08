# Hotfix derived from the published API image, without unrelated source changes.
ARG API_BASE_IMAGE=xjensu/table-api:2026-10-06-1
FROM ${API_BASE_IMAGE}
RUN ruby -e 'p="/app/lib/api_geteway/media/sanitizers/virus_scanner.rb"; s=File.read(p); abort "Unexpected scanner source" unless s.include?("Clamby.clamscan?"); File.write(p, s.sub("Clamby.clamscan?", "Clamby.scanner_exists?").sub(%q{require "clamby"}, %Q{require "shellwords"\nrequire "clamby"}))'
