#!/usr/bin/env python3
"""Refresh signed ClamAV data from a maintained mirror, with official-image bootstrap."""
import fcntl
import json
from pathlib import Path
import re
import subprocess
import urllib.request
import urllib.error
import urllib.parse
import time

ROOT = Path(__file__).resolve().parents[2]

def run(args, timeout=60):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f'{args[0]} failed (exit {result.returncode}); inspect service/network privately')
    return result.stdout


def mirror_databases(directory, mirror):
    parsed = urllib.parse.urlsplit(mirror)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise RuntimeError('Signature mirror must be an HTTPS base URL without embedded credentials')
    cache = directory / 'signature-cache'
    cache.mkdir(exist_ok=True, mode=0o700)
    metadata_path = cache / 'metadata.json'
    metadata = json.loads(metadata_path.read_text()) if metadata_path.exists() else {}
    updated = {}
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    deadline = time.monotonic() + 300
    for name in ('main.cvd', 'daily.cvd', 'bytecode.cvd'):
        url = mirror.rstrip('/') + '/' + name
        target = cache / name
        headers = {}
        previous = metadata.get(url, {})
        if target.is_file() and previous.get('modified'):
            headers['If-Modified-Since'] = previous['modified']
        try:
            response = opener.open(urllib.request.Request(url, headers=headers), timeout=30)
        except urllib.error.HTTPError as error:
            if error.code == 304 and target.is_file():
                updated[url] = previous
                continue
            raise
        temporary = target.with_suffix('.download')
        try:
            size = 0
            with response, temporary.open('wb') as stream:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > 256 * 1024 * 1024 or time.monotonic() > deadline:
                        raise RuntimeError('Signature download exceeded size/time bounds')
                    stream.write(chunk)
                if size == 0:
                    raise RuntimeError('Empty signature database')
                updated[url] = {'modified': response.headers.get('Last-Modified', '')}
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    return cache, metadata_path, updated


def main():
    folder = ROOT / 'deploy/generated/recovery'
    folder.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (folder / 'signature-refresh.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return
        config = json.loads(run([str(ROOT / 'deploy/bin/compose.sh'), 'config', '--format', 'json']))
        service = config['services']['clamav_signatures']
        image = service.get('environment', {}).get('CLAMAV_SEED_IMAGE', 'clamav/clamav:1.5')
        if not re.fullmatch(r'clamav/clamav(?::[A-Za-z0-9_.-]+|@sha256:[a-f0-9]{64})', image):
            raise RuntimeError('Seed source must be an official clamav/clamav image')
        ids = run(['docker', 'ps', '-q', '--filter', f'label=com.docker.compose.project={config["name"]}',
                   '--filter', 'label=com.docker.compose.service=clamav_signatures']).split()
        if not ids:
            print('Signature updater is intentionally stopped/absent; no action taken.')
            return
        container = json.loads(run(['docker', 'inspect', ids[0]]))[0]
        mounts = [x for x in container['Mounts'] if x['Destination'] == '/signatures' and x['Type'] == 'volume']
        if len(mounts) != 1:
            raise RuntimeError('Expected exactly one named signature volume')
        try:
            run(['docker', 'pull', image], timeout=600)
        except (RuntimeError, subprocess.TimeoutExpired):
            print('Registry pull unavailable; attempting the existing official verifier image.', flush=True)
        digests = json.loads(run(['docker', 'image', 'inspect', image]))[0]['RepoDigests']
        digest = next((item for item in digests if item.startswith('clamav/clamav@')), None)
        if not digest:
            raise RuntimeError('Official image digest unavailable')
        print('Official signature image:', digest, flush=True)
        mirror = service.get('environment', {}).get('CLAMAV_DATABASE_MIRROR', 'https://packages.microsoft.com/clamav')
        source_mount = []
        metadata = None
        try:
            cache, metadata_path, metadata = mirror_databases(folder, mirror)
            source_mount = ['-v', str(cache) + ':/var/lib/clamav:ro']
            print('Downloaded/cached mirror data; cryptographic verification required before installation.', flush=True)
        except (OSError, ValueError, RuntimeError, urllib.error.URLError) as error:
            print(f'Mirror unavailable ({type(error).__name__}); trying verified official-image bootstrap.', flush=True)
        output = run(['docker', 'run', '--rm', '--network', 'none', '--read-only',
                      '-v', mounts[0]['Name'] + ':/signatures',
                      '-v', str(ROOT / 'deploy/antivirus/update-signatures.sh') + ':/seed.sh:ro',
                      *source_mount,
                      '--entrypoint', 'sh', digest, '/seed.sh', '--seed-only'], timeout=300)
        if metadata is not None:
            metadata_path.write_text(json.dumps(metadata))
        print(output.strip(), flush=True)
        # The embedded build date remains the acceptance gate. Registry age is not assumed.
        run(['docker', 'exec', ids[0], 'sh', '/opt/antivirus/check-signatures.sh'])
        print('Signature freshness: PASS; existing API/scanners use the shared volume immediately.')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.TimeoutExpired) as error:
        raise SystemExit(f'Signature refresh failed: {error}')
