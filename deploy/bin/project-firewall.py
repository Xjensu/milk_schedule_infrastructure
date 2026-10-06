#!/usr/bin/env python3
"""Idempotent Docker-aware filtering limited to this project's containers."""
import ipaddress
import json
import os
import shlex
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
settings = json.loads((ROOT / "deploy/generated/network.json").read_text())

def cmd(*args, check=True):
    return subprocess.run(args, check=check, capture_output=True, text=True)

if os.geteuid() != 0:
    raise SystemExit("Run this project firewall installer as root; unrelated host rules are preserved.")
# Refuse to claim protection when Docker uses a different backend.
if cmd("iptables", "-S", "DOCKER-USER", check=False).returncode:
    raise SystemExit("Docker DOCKER-USER chain unavailable. Configure the supported iptables backend before public deployment.")
chain = "MILK_INGRESS"
cmd("iptables", "-N", chain, check=False)
cmd("iptables", "-F", chain)
cmd("iptables", "-A", chain, "-m", "conntrack", "--ctstate", "ESTABLISHED,RELATED", "-j", "RETURN")
cmd("iptables", "-A", chain, "-s", settings["discovery_subnet"], "-j", "RETURN")
# Scope rules to project destination networks only; nothing else is modified.
containers = json.loads((ROOT / "deploy/generated/firewall-containers.json").read_text())
for container in containers:
    service = container["service"]
    for destination in container["addresses"]:
        if not destination:
            continue
        if service == "nginx":
            cmd("iptables", "-A", chain, "-d", destination, "-p", "tcp", "--dport", "80", "-j", "RETURN")
        elif service == "minio":
            for cidr in settings["cidrs"]:
                if ipaddress.ip_network(cidr).version == 4:
                    cmd("iptables", "-A", chain, "-s", cidr, "-d", destination, "-p", "tcp", "--dport", "9000", "-j", "RETURN")
            cmd("iptables", "-A", chain, "-d", destination, "-p", "tcp", "--dport", "9000", "-j", "DROP")
cmd("iptables", "-A", chain, "-d", settings["discovery_subnet"], "-j", "DROP")
cmd("iptables", "-A", chain, "-j", "RETURN")
if cmd("iptables", "-C", "DOCKER-USER", "-j", chain, check=False).returncode:
    cmd("iptables", "-I", "DOCKER-USER", "1", "-j", chain)
# Docker's userland port proxy receives connections through INPUT rather than
# FORWARD. Protect the selected host-bound storage port on both paths.
host_chain = "MILK_HOST"
cmd("iptables", "-N", host_chain, check=False)
cmd("iptables", "-F", host_chain)
for cidr in settings["cidrs"]:
    if ipaddress.ip_network(cidr).version == 4:
        cmd("iptables", "-A", host_chain, "-s", cidr, "-j", "RETURN")
cmd("iptables", "-A", host_chain, "-j", "DROP")
host_rule = ("-d", settings["address"], "-p", "tcp", "--dport", "9000", "-j", host_chain)
for line in cmd("iptables", "-S", "INPUT").stdout.splitlines():
    rule = shlex.split(line)
    if "-j" in rule and rule[rule.index("-j") + 1] == host_chain:
        cmd("iptables", "-D", *rule[1:])
if cmd("iptables", "-C", "INPUT", *host_rule, check=False).returncode:
    cmd("iptables", "-I", "INPUT", "1", *host_rule)
print("Project ingress firewall installed; SSH and unrelated services preserved.")
