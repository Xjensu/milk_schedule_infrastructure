#!/usr/bin/env python3
"""One bounded, project-scoped recovery sweep. Run via the installed systemd timer."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = [str(ROOT / 'deploy/bin/compose.sh')]
LABEL = 'by.bsut.recovery'


def run(args):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=45)
    if result.returncode:
        # Expanded Compose/Docker output can contain secrets. Do not log it.
        raise RuntimeError(f'{args[0]} failed with exit code {result.returncode}')
    return result.stdout


def sweep(state, config, containers, now, restart):
    services = config['services']
    project = config['name']
    grouped = {}
    for container in containers:
        labels = container['Config'].get('Labels') or {}
        if labels.get('com.docker.compose.project') == project:
            grouped.setdefault(labels.get('com.docker.compose.service'), []).append(container)
    for name, replicas in grouped.items():
        definition = services.get(name, {})
        if definition.get('labels', {}).get(LABEL) != 'unhealthy':
            continue
        for container in replicas:
            identity = container['Id']
            current = container['State']
            # Respect manual stops, paused containers, one-shot jobs and missing services.
            if not current.get('Running') or current.get('Paused'):
                state.pop(identity, None)
                continue
            item = state.setdefault(identity, {'attempts': []})
            item['attempts'] = [stamp for stamp in item['attempts'] if now - stamp < 3600]
            if current.get('Health', {}).get('Status') != 'unhealthy':
                item.pop('since', None)
                continue
            item.setdefault('since', now)
            if now - item['since'] < 120:
                continue
            dependencies = definition.get('depends_on', {})
            blocked = []
            for dependency, rule in dependencies.items():
                if rule.get('condition') != 'service_healthy':
                    continue
                instances = grouped.get(dependency, [])
                if not instances or not all(x['State'].get('Running') and
                        not x['State'].get('Paused') and
                        x['State'].get('Health', {}).get('Status') == 'healthy' for x in instances):
                    blocked.append(dependency)
            if blocked:
                print(f'{name}: waiting for dependencies: {", ".join(blocked)}', flush=True)
                continue
            attempts = item['attempts']
            cooldown = min(1800, 300 * (2 ** max(0, len(attempts) - 1)))
            if len(attempts) >= 3 or (attempts and now - attempts[-1] < cooldown):
                print(f'{name}: recovery budget/cooldown active; inspect service logs', flush=True)
                continue
            print(f'{name}: restarting persistently unhealthy container {identity[:12]}', flush=True)
            # Record BEFORE mutation, even if Docker times out or this process is interrupted.
            attempts.append(now)
            item['since'] = now
            restart(identity, state)
    live_ids = {x['Id'] for x in containers}
    for identity in list(state):
        if identity not in live_ids:
            del state[identity]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    directory = ROOT / 'deploy/generated/recovery'
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(directory, 0o700)
    with (directory / 'lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        config = json.loads(run([*COMPOSE, 'config', '--format', 'json']))
        ids = run(['docker', 'ps', '-aq', '--filter', f'label=com.docker.compose.project={config["name"]}']).split()
        if not ids:
            return
        containers = json.loads(run(['docker', 'inspect', *ids]))
        path = directory / 'state.json'
        # Invalid state fails closed instead of silently resetting the restart budget.
        state = json.loads(path.read_text()) if path.exists() else {}

        def save(value):
            if args.dry_run:
                return
            temp = path.with_suffix('.tmp')
            temp.write_text(json.dumps(value))
            temp.chmod(0o600)
            temp.replace(path)

        def restart(identity, value):
            if args.dry_run:
                print('dry-run: no restart performed', flush=True)
                return
            save(value)
            run(['docker', 'restart', '--time', '20', identity])

        sweep(state, config, containers, time.time(), restart)
        save(state)


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.TimeoutExpired) as error:
        raise SystemExit(f'Recovery sweep failed ({type(error).__name__}); inspect Docker/configuration privately.')
