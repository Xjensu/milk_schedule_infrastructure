#!/usr/bin/env python3
"""Install/update a project-specific host timer; no Docker socket in web containers."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--remove', action='store_true')
parser.add_argument('--dry-run', action='store_true', help='Print generated units as JSON without changing the host')
args = parser.parse_args()
if os.geteuid() != 0 and not args.dry_run:
    raise SystemExit('Run with sudo python3 deploy/bin/install-recovery.py')
if not args.dry_run and not Path('/run/systemd/system').exists():
    raise SystemExit('A systemd Linux host is required; see the recovery guide for a cron alternative.')
# Unit names are stable per checkout, avoiding cross-project collisions.
name = 'milk-recovery-' + hashlib.sha256(str(ROOT).encode()).hexdigest()[:12]
units = Path('/etc/systemd/system')
if args.remove and args.dry_run:
    raise SystemExit('--remove and --dry-run cannot be combined')
if args.remove:
    subprocess.run(['systemctl', 'disable', '--now', name + '.timer'], check=True)
    subprocess.run(['systemctl', 'stop', name + '.service'], check=True)
    for suffix in ('.timer', '.service'):
        (units / (name + suffix)).unlink(missing_ok=True)
    subprocess.run(['systemctl', 'daemon-reload'], check=True)
    print(f'Removed {name}')
else:
    # systemd expands %, $, and backslashes separately from shell quoting.
    if any(c in str(ROOT) for c in '\n\r"\\'):
        raise SystemExit('Use a checkout path without quotes, backslashes or newlines.')
    escaped = str(ROOT).replace('%', '%%').replace('$', '$$')
    service = f'''[Unit]
Description=Bounded unhealthy-container recovery for milk schedule
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
WorkingDirectory={str(ROOT).replace("%", "%%")}
ExecStart=/usr/bin/python3 "{escaped}/deploy/bin/recover-services.py"
TimeoutStartSec=180
UMask=0077
Nice=10
'''
    timer = f'''[Unit]
Description=Check milk schedule container health every 30 seconds

[Timer]
OnBootSec=90
OnUnitInactiveSec=30
AccuracySec=5
Unit={name}.service

[Install]
WantedBy=timers.target
'''
    if args.dry_run:
        print(json.dumps({name + '.service': service, name + '.timer': timer}))
        raise SystemExit(0)
    (units / (name + '.service')).write_text(service)
    (units / (name + '.timer')).write_text(timer)
    subprocess.run(['systemctl', 'daemon-reload'], check=True)
    subprocess.run(['systemctl', 'enable', '--now', name + '.timer'], check=True)
    print(f'Installed {name}.timer; logs: journalctl -u {name}.service')
