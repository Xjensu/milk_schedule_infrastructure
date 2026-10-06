"""Idempotently provision scoped tokens; secret values are never emitted."""
import json
import time
from pathlib import Path
from urllib.request import Request, build_opener, ProxyHandler

base = "http://consul:8500"
files = Path("/run/credentials")
admin = (files / "consul-management.token").read_text().strip()
opener = build_opener(ProxyHandler({}))

def call(path, data=None, method="GET"):
    req = Request(base + path, data=None if data is None else json.dumps(data).encode(), method=method,
                  headers={"X-Consul-Token": admin, "Content-Type": "application/json"})
    with opener.open(req, timeout=3) as response:
        raw = response.read()
        return json.loads(raw) if raw else None

for attempt in range(60):
    try:
        if call("/v1/status/leader"):
            break
    except Exception:
        pass
    time.sleep(2)
else:
    raise SystemExit("Consul did not become ready")

deps = {
    "schedule-web": ["api-geteway", "redis"],
    "api-geteway": ["postgres", "redis", "minio", "scheduler"],
    "scheduler": ["api-geteway"],
    "ops-console": ["postgres"],
    "outbox-relay": ["postgres", "redis", "minio"],
    "media-sanitizer": ["postgres", "redis", "minio"],
    "notice-export-worker": ["postgres", "redis", "minio"],
    "schedule-generation-worker": ["postgres", "redis", "minio", "scheduler"],
    "excel-processor": ["postgres", "redis", "minio"],
    "nginx": ["schedule-web", "api-geteway", "ops-console"],
    "postgres": [], "redis": [], "minio": [], "minio-init": ["minio"],
}
policies = {p["Name"]: p["ID"] for p in call("/v1/acl/policies")}
tokens = {t["Description"]: t for t in call("/v1/acl/tokens")}
for service, dependencies in deps.items():
    name = "milk-" + service
    rules = 'node_prefix "" { policy = "read" }\n'
    rules += f'service "{service}" {{ policy = "write" }}\n'
    rules += "".join(f'service "{dependency}" {{ policy = "read" }}\n' for dependency in dependencies)
    body = {"Name": name, "Description": "Milk scoped service discovery", "Rules": rules}
    if name in policies:
        body["ID"] = policies[name]
    policy = call("/v1/acl/policy" + ("/" + policies[name] if name in policies else ""), body, "PUT")
    token = {"Description": name, "SecretID": (files / (service + ".token")).read_text().strip(),
             "Policies": [{"ID": policy["ID"]}]}
    if name in tokens:
        token["AccessorID"] = tokens[name]["AccessorID"]
    call("/v1/acl/token" + ("/" + tokens[name]["AccessorID"] if name in tokens else ""), token, "PUT")
print("Consul scoped ACL policies ready")
