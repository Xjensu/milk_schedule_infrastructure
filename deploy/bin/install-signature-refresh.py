#!/usr/bin/env python3
"""Install a six-hourly verified signature refresh; supports system and user timers."""
import argparse
import hashlib
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--user', action='store_true', help='Use this user\'s Docker access/systemd manager')
parser.add_argument('--remove', action='store_true')
args = parser.parse_args()
if not args.user and os.geteuid() != 0:
    raise SystemExit('Use sudo, or --user with Docker access and a working user systemd manager.')
if any(c in str(ROOT) for c in '\n\r"\\'):
    raise SystemExit('Unsupported checkout path')
name = 'milk-signatures-' + hashlib.sha256(str(ROOT).encode()).hexdigest()[:12]
manager = ['systemctl'] + (['--user'] if args.user else [])
directory = Path.home() / '.config/systemd/user' if args.user else Path('/etc/systemd/system')
directory.mkdir(parents=True, exist_ok=True)
if args.remove:
    subprocess.run([*manager, 'disable', '--now', name + '.timer'], check=True)
    subprocess.run([*manager, 'stop', name + '.service'], check=True)
    for suffix in ('.service', '.timer'):
        (directory / (name + suffix)).unlink(missing_ok=True)
else:
    escaped = str(ROOT).replace('%', '%%').replace('$', '$$')
    dependency = '' if args.user else 'After=docker.service\nRequires=docker.service\n'
    (directory / (name + '.service')).write_text(f'''[Unit]
Description=Refresh verified ClamAV signatures from a maintained mirror
{dependency}
[Service]
Type=oneshot
WorkingDirectory={str(ROOT).replace('%', '%%')}
ExecStart=/usr/bin/python3 "{escaped}/deploy/bin/refresh-signatures.py"
TimeoutStartSec=1200
UMask=0077
''')
    (directory / (name + '.timer')).write_text(f'''[Unit]
Description=Refresh signed ClamAV databases every six hours

[Timer]
OnBootSec=120
OnUnitInactiveSec=6h
AccuracySec=1min
Unit={name}.service

[Install]
WantedBy=timers.target
''')
subprocess.run([*manager, 'daemon-reload'], check=True)
if not args.remove:
    subprocess.run([*manager, 'enable', '--now', name + '.timer'], check=True)
print(('Removed ' if args.remove else 'Installed ') + name + '.timer')
