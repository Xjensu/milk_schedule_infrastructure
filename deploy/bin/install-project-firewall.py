#!/usr/bin/env python3
"""Apply project rules using sudo, or an ephemeral NET_ADMIN Docker helper."""
import json
import os
import shutil
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parents[2]
compose = [str(ROOT / "deploy/bin/compose.sh")]
ids = subprocess.check_output([*compose, "ps", "-q", "nginx", "minio"], cwd=ROOT, text=True).split()
if len(ids) != 2:
    raise SystemExit("Start Nginx and MinIO before installing ingress rules.")
containers = json.loads(subprocess.check_output(["docker", "inspect", *ids], text=True))
# Persist only networking fields, never Docker's complete configuration/environment.
safe = [{"service": x["Config"]["Labels"]["com.docker.compose.service"],
         "addresses": [n["IPAddress"] for n in x["NetworkSettings"]["Networks"].values() if n["IPAddress"]]} for x in containers]
path = ROOT / "deploy/generated/firewall-containers.json"
path.write_text(json.dumps(safe))
os.chmod(path, 0o600)
script = str(ROOT / "deploy/bin/project-firewall.py")
if os.geteuid() == 0:
    subprocess.run(["python3", script], check=True)
elif shutil.which("sudo") and subprocess.run(["sudo", "-n", "true"], capture_output=True).returncode == 0:
    subprocess.run(["sudo", "-n", "python3", script], check=True)
else:
    # This helper alone has NET_ADMIN. Application and registration containers do not.
    image = next(x["Image"] for x in containers if x["Config"]["Labels"]["com.docker.compose.service"] == "nginx")
    subprocess.run(["docker", "run", "--rm", "--entrypoint", "sh", "--network", "host", "--cap-add", "NET_ADMIN",
                    "-v", str(ROOT) + ":/workspace:ro", image, "-ec",
                    "python3 /workspace/deploy/bin/project-firewall.py"], check=True)
