#!/usr/bin/env python3
"""Remove only retired infrastructure containers in this Compose project, never volumes."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
compose = str(ROOT / "deploy/bin/compose.sh")
# Expanded configuration stays in memory; it can contain credentials.
config = json.loads(subprocess.check_output([compose, "config", "--format", "json"], text=True))
project = config["name"]
retired = {"consul", "discovery_acl", "postgres_registrar", "redis_registrar", "minio_registrar",
           "frontend", "solr"}
for service in sorted(retired):
    ids = subprocess.check_output([
        "docker", "ps", "-aq", "--filter", f"label=com.docker.compose.project={project}",
        "--filter", f"label=com.docker.compose.service={service}",
    ], text=True).split()
    if ids:
        subprocess.run(["docker", "stop", "--timeout", "20", *ids], check=True)
        subprocess.run(["docker", "rm", *ids], check=True)
        print(f"Retired {service}: {len(ids)} container(s); volumes preserved.")
