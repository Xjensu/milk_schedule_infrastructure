#!/usr/bin/env python3
"""Package only the files required by an image-only server deployment."""
import argparse
import io
import json
import os
import re
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("tag", help="The immutable tag used to build/push this release")
parser.add_argument("--namespace", default="xjensu", help="Registry namespace used for the build")
args = parser.parse_args()
if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}", args.tag):
    parser.error("invalid Docker image tag")
if not re.fullmatch(r"[a-z0-9][a-z0-9./:_-]*", args.namespace):
    parser.error("invalid registry namespace")

files = [
    "docker-compose.yml", ".env.compose.example", ".env.example", "README.md",
    "deploy/DEPLOYMENT_GUIDE.md", "deploy/SERVICE_DISCOVERY.md",
    "deploy/ops/.env.example", "deploy/ops/README.md", "deploy/edge/denylist.geo",
    *["deploy/bin/" + name for name in (
        "compose.sh", "db.sh", "init-env.py", "prepare-discovery.py", "deploy-discovery.sh",
        "install-project-firewall.py", "project-firewall.py")],
]
for pattern in (
    "deploy/discovery/python/*.py", "deploy/discovery/ruby/*.rb", "schemas/avro/*.avsc",
    "schemas/protobuf/*.proto", "deploy/observability/**/*.yml",
    "deploy/observability/**/*.json", "deploy/observability/**/*.conf",
):
    files.extend(str(p.relative_to(ROOT)) for p in ROOT.glob(pattern))
files.extend(["deploy/observability/.env.example", "deploy/observability/README.md"])

environment = {**os.environ, "IMAGE_TAG": args.tag, "IMAGE_NAMESPACE": args.namespace}
images = subprocess.check_output([
    "docker", "compose", "--env-file", str(ROOT / ".env.compose.example"),
    "-f", str(ROOT / "compose.build.yml"), "--profile", "*", "config", "--images",
], env=environment, text=True).splitlines()
revisions = {}
for name in (".", "apps/schedule_web", "apps/api_geteway", "apps/excel_processor", "apps/frontend"):
    revisions[name] = {
        "commit": subprocess.check_output(["git", "-C", str(ROOT / name), "rev-parse", "HEAD"], text=True).strip(),
        "dirty": bool(subprocess.check_output(["git", "-C", str(ROOT / name), "status", "--porcelain"], text=True)),
    }
manifest = {"tag": args.tag, "namespace": args.namespace, "custom_images": images, "sources": revisions}
destination = ROOT / "dist" / f"milk-schedule-{args.tag}.tar.gz"
destination.parent.mkdir(exist_ok=True)


def add_bytes(archive, name, content):
    entry = tarfile.TarInfo(name)
    entry.size = len(content)
    entry.mode = 0o644
    archive.addfile(entry, io.BytesIO(content))


with tarfile.open(destination, "w:gz") as archive:
    for name in sorted(set(files)):
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            raise SystemExit(f"Missing or non-regular release file: {name}")
        if name in (".env.compose.example", ".env.example"):
            content = path.read_text()
            for key, value in (("IMAGE_TAG", args.tag), ("IMAGE_NAMESPACE", args.namespace)):
                content = re.sub(rf"^{key}=.*$", lambda _: f"{key}={value}", content, flags=re.M)
            add_bytes(archive, name, content.encode())
        else:
            archive.add(path, arcname=name, recursive=False)
    add_bytes(archive, "RELEASE.json", (json.dumps(manifest, indent=2) + "\n").encode())
print(f"Created {destination.relative_to(ROOT)}; {len(set(files))} deployment files, no local secrets or application source.")
if any(r["dirty"] for r in revisions.values()):
    print("Source worktrees contain uncommitted changes; RELEASE.json records this. Build and package the same worktree state.")
