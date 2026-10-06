#!/usr/bin/env python3
"""Create private configuration once; never overwrite existing credentials."""
import os
import re
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.umask(0o077)


def create(template, destination, replacements):
    path = ROOT / destination
    if path.exists():
        print(f"Kept existing {destination}")
        return
    text = (ROOT / template).read_text()
    for key, value in replacements.items():
        text = re.sub(rf"^{key}=.*$", lambda _: f"{key}={value}", text, flags=re.M)
    with path.open("x") as stream:
        stream.write(text)
    print(f"Created {destination} (private; values not printed)")


create(".env.example", ".env.local", {
    key: secrets.token_hex(64 if key == "SECRET_KEY_BASE" else 32)
    for key in ("POSTGRES_PASSWORD", "REDIS_PASSWORD", "MINIO_SECRET_KEY",
                "JWT_SECRET", "SECRET_KEY_BASE", "SEED_ADMIN_PASSWORD")
})
create("deploy/ops/.env.example", "deploy/ops/.env.local", {
    "OPS_CONSOLE_PASSWORD": secrets.token_hex(32),
})
create("deploy/observability/.env.example", "deploy/observability/.env.local", {
    "GF_SECURITY_ADMIN_PASSWORD": secrets.token_hex(32),
})
print("Review the image tag, administrator email and browser origin in .env.local before deployment.")
