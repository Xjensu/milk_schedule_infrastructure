"""Consul registration and bounded runtime endpoint discovery (no secret logging)."""
import ipaddress
import json
import os
import socket
import threading
import time
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, quote
from urllib.request import Request, build_opener, ProxyHandler


class Unavailable(RuntimeError):
    pass


_cache = {}
_lock = threading.Lock()
_opener = build_opener(ProxyHandler({}))


def enabled():
    return os.environ.get("DISCOVERY_ENABLED") == "1"


def request(path, payload=None, method="GET"):
    token = Path(os.environ["CONSUL_TOKEN_FILE"]).read_text().strip()
    req = Request(os.environ["CONSUL_HTTP_ADDR"].rstrip("/") + path,
                  data=None if payload is None else json.dumps(payload).encode(), method=method,
                  headers={"X-Consul-Token": token, "Content-Type": "application/json"})
    with _opener.open(req, timeout=2) as response:
        data = response.read()
        return json.loads(data) if data else None


def instances(service):
    now = time.monotonic()
    with _lock:
        cached = _cache.get(service)
    if cached and now - cached[0] < 5:
        if not cached[1]:
            raise Unavailable(f"No healthy {service} instance")
        return cached[1]
    try:
        rows = request("/v1/health/service/" + quote(service, safe="") + "?passing=true")
        found = []
        for row in rows:
            svc = row["Service"]
            address = str(ipaddress.ip_address(svc["Address"]))
            port = int(svc["Port"])
            if not 0 < port < 65536:
                raise ValueError("invalid service port")
            found.append((address, port))
        found = sorted(set(found))
    except Exception:
        if cached and cached[1] and now - cached[0] < 60:
            return cached[1]
        raise Unavailable(f"Discovery unavailable for {service}") from None
    with _lock:
        _cache[service] = (time.monotonic(), found)
    if not found:
        raise Unavailable(f"No healthy {service} instance")
    return found


def endpoint(service, scheme="http"):
    address, port = instances(service)[0]
    return f"{scheme}://{address}:{port}"


def database_url():
    if not enabled():
        return os.environ["DATABASE_URL"]
    address, port = instances("postgres")[0]
    return (f"postgresql://{quote(os.environ['POSTGRES_USER'], safe='')}:"
            f"{quote(os.environ['POSTGRES_PASSWORD'], safe='')}@{address}:{port}/"
            f"{quote(os.environ['POSTGRES_DB'], safe='')}")


def wait_for(*services):
    deadline = time.monotonic() + 120
    for service in services:
        while True:
            try:
                instances(service)
                break
            except Unavailable:
                if time.monotonic() >= deadline:
                    raise Unavailable("Discovery startup deadline exceeded") from None
                time.sleep(2)


def advertised_address():
    target = urlsplit(os.environ["CONSUL_HTTP_ADDR"])
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.connect((socket.gethostbyname(target.hostname), target.port or 8500))
        return sock.getsockname()[0]


def register(stop, healthy):
    service = os.environ["DISCOVERY_SERVICE"]
    instance = service + "-" + socket.gethostname()
    check = "service:" + instance
    while not stop.is_set():
        try:
            request("/v1/agent/service/register", {
                "ID": instance, "Name": service, "Address": advertised_address(),
                "Port": int(os.environ.get("DISCOVERY_PORT", "0")),
                "Meta": {"revision": os.environ.get("APP_REVISION", "unknown")},
                "Check": {"TTL": "15s", "DeregisterCriticalServiceAfter": "2m"}
            }, "PUT")
            request("/v1/agent/check/" + ("pass/" if healthy() else "fail/") + check, method="PUT")
        except Exception:
            pass
        stop.wait(5)
    try:
        request("/v1/agent/service/deregister/" + instance, method="PUT")
    except Exception:
        pass


def start_registration(healthy):
    if not enabled():
        return None
    stop = threading.Event()
    thread = threading.Thread(target=register, args=(stop, healthy), daemon=True)
    thread.start()
    return stop
