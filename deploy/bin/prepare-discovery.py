#!/usr/bin/env python3
"""Generate host-specific ingress policy and private Consul credentials."""
import ipaddress
import json
import os
import re
import shlex
import subprocess
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "deploy/generated"
OUT.mkdir(mode=0o700, parents=True, exist_ok=True)
os.chmod(OUT, 0o700)
addresses = json.loads(subprocess.check_output(["ip", "-j", "-4", "address", "show"], text=True))
routes = json.loads(subprocess.check_output(["ip", "-j", "-4", "route", "show"], text=True))
settings = {}
for filename in (".env", ".env.local"):
    path = ROOT / filename
    if not path.exists():
        continue
    for line in path.read_text().splitlines():
        key, separator, value = line.partition("=")
        if separator and key.strip() in ("ADMIN_INTERFACE", "ADMIN_LAN_CIDRS", "LAN_BIND_IP"):
            parts = shlex.split(value, comments=True)
            if len(parts) > 1:
                raise SystemExit(f"Invalid {key.strip()} in {filename}; use one value without spaces.")
            settings[key.strip()] = parts[0] if parts else ""
interface = os.environ.get("ADMIN_INTERFACE", settings.get("ADMIN_INTERFACE", ""))
explicit = os.environ.get("ADMIN_LAN_CIDRS", settings.get("ADMIN_LAN_CIDRS", ""))
bind_ip = os.environ.get("LAN_BIND_IP", settings.get("LAN_BIND_IP", ""))
private = [ipaddress.ip_network(n) for n in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")]
candidates = []
for item in addresses:
    name = item["ifname"]
    if interface and name != interface:
        continue
    if not interface and not bind_ip and (re.match(r"^(lo$|docker|br-|veth|virbr|tun|tap|wg|tailscale|zt)", name) or item.get("link_type") == "none"):
        continue
    for address in item.get("addr_info", []):
        value = ipaddress.ip_address(address["local"])
        if bind_ip and str(value) != bind_ip:
            continue
        if address.get("scope") == "global" and (bind_ip or any(value in network for network in private)):
            candidates.append((name, ipaddress.ip_interface(f"{value}/{address['prefixlen']}")))
if len(candidates) > 1 and not interface and not bind_ip:
    # A routing lookup sends no traffic and selects the normal outbound address.
    try:
        outbound = json.loads(subprocess.check_output(
            ["ip", "-j", "-4", "route", "get", "1.1.1.1"], text=True
        ))
    except subprocess.CalledProcessError:
        outbound = []
    preferred = [candidate for candidate in candidates if any(
        route.get("dev") == candidate[0]
        and route.get("prefsrc") == str(candidate[1].ip)
        for route in outbound
    )]
    if len(preferred) == 1:
        candidates = preferred
if len(candidates) != 1:
    raise SystemExit("Could not identify a unique LAN interface automatically. Check the host's IPv4/default route or set ADMIN_INTERFACE in .env.local; no policy was expanded.")
name, selected = candidates[0]
if not explicit and not any(selected.ip in network for network in private):
    raise SystemExit("A public bind address requires explicit ADMIN_LAN_CIDRS for trusted client addresses.")
cidrs = [ipaddress.ip_network(x.strip(), strict=False) for x in explicit.split(",") if x.strip()] or [selected.network]
if any(net.version != 4 for net in cidrs):
    raise SystemExit("This deployment supports IPv4 administrator CIDRs only.")
if any(net.prefixlen == 0 for net in cidrs):
    raise SystemExit("A default-route administrator allowlist is prohibited.")
used = [ipaddress.ip_network(r["dst"], strict=False) for r in routes if r.get("dst") not in (None, "default")]
for network in range(246, 200, -1):
    discovery = ipaddress.ip_network(f"172.28.{network}.0/24")
    # Preserve our existing subnet across subsequent deployments.
    existing = OUT / "compose.env"
    if existing.exists():
        match = re.search(r"^DISCOVERY_SUBNET=(.+)$", existing.read_text(), re.M)
        if match:
            discovery = ipaddress.ip_network(match[1])
            break
    if not any(discovery.overlaps(net) for net in used):
        break
else:
    raise SystemExit("No free discovery subnet; choose another host network allocation.")

def write(name, content, mode=0o600):
    path = OUT / name
    if path.exists():
        os.chmod(path, 0o600)
    path.write_text(content)
    os.chmod(path, mode)

services = ["schedule-web", "api-geteway", "scheduler", "ops-console", "outbox-relay", "media-sanitizer",
            "notice-export-worker", "schedule-generation-worker", "excel-processor", "postgres", "redis", "minio", "nginx", "minio-init"]
for service in ["consul-management", *services]:
    path = OUT / (service + ".token")
    if not path.exists():
        write(path.name, str(uuid.uuid4()) + "\n", 0o444)
management = (OUT / "consul-management.token").read_text().strip()
write("consul.hcl", f'''datacenter = "milk"
node_name = "milk-consul"
server = true
bootstrap_expect = 1
data_dir = "/consul/data"
client_addr = "0.0.0.0"
bind_addr = "0.0.0.0"
ui_config {{ enabled = false }}
log_level = "warn"
acl {{
  enabled = true
  default_policy = "deny"
  enable_token_persistence = true
  tokens {{ initial_management = "{management}" agent = "{management}" }}
}}
''', 0o444)
write("compose.env", f"LAN_BIND_IP={selected.ip}\nLAN_CIDR={cidrs[0]}\nLAN_CIDRS={','.join(str(n) for n in cidrs)}\nDISCOVERY_SUBNET={discovery}\nDISCOVERY_IP_RANGE={list(discovery.subnets(prefixlen_diff=1))[1]}\nINGRESS_IP={discovery.network_address + 2}\nCONSUL_IP={discovery.network_address + 3}\n", 0o600)
# LAN policy uses Nginx's direct peer address; Docker networks are never allowlisted.
write("lan.geo", "geo $trusted_lan {\n  default 0;\n" + "".join(f"  {net} 1;\n" for net in cidrs) + "  127.0.0.1/32 1;\n}\n", 0o444)
write("network.json", json.dumps({"interface": name, "address": str(selected.ip), "cidrs": [str(n) for n in cidrs],
                                   "discovery_subnet": str(discovery)}, indent=2) + "\n")
print(f"Prepared LAN {selected.network} on {name}; configuration in deploy/generated (secrets not printed).")
