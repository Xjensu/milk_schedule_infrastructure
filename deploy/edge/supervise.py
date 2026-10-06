"""Validate discovered upstreams, supervise Nginx, and enforce cache expiry."""
import hashlib
import ipaddress
import os
from pathlib import Path
import signal
import subprocess
import threading
import time
from discovery import request, start_registration

stop = threading.Event()
for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, lambda *_: stop.set())
run = Path("/run/nginx")
run.mkdir(parents=True, exist_ok=True)
active = run / "upstreams.conf"
fallback = "".join(f"upstream {name} {{ server 127.0.0.1:9 down; }}\n" for name in ("rails_web", "hanami_api", "ops_service"))
active.write_text(fallback)
if subprocess.run(["nginx", "-t"], capture_output=True).returncode:
    raise SystemExit("Invalid base Nginx configuration")
nginx = subprocess.Popen(["nginx", "-g", "daemon off;"])
environment = os.environ.copy()
environment["CONSUL_HTTP_TOKEN"] = Path(environment["CONSUL_TOKEN_FILE"]).read_text().strip()
ct = subprocess.Popen(["consul-template", "-consul-addr=" + environment["CONSUL_HTTP_ADDR"].removeprefix("http://"),
                       "-template=/etc/nginx/upstreams.ctmpl:/run/nginx/candidate.conf", "-log-level=err"], env=environment)
registration = start_registration(lambda: nginx.poll() is None)
last_verified = 0.0
applied = fallback
try:
    while not stop.wait(2):
        if nginx.poll() is not None or ct.poll() is not None:
            raise RuntimeError("Ingress child process exited")
        verified = False
        healthy = {}
        try:
            for name in ("schedule-web", "api-geteway", "ops-console"):
                entries = request("/v1/health/service/" + name + "?passing=true")
                healthy[name] = {(str(ipaddress.ip_address(e["Service"]["Address"])), int(e["Service"]["Port"])) for e in entries}
            last_verified = time.monotonic()
            verified = True
        except Exception:
            pass
        candidate = run / "candidate.conf"
        text = candidate.read_text() if candidate.exists() else fallback
        if time.monotonic() - last_verified >= 60:
            text = fallback
        elif verified:
            # An empty health result must stop routing immediately, even before CT catches up.
            import re
            for service, upstream in (("schedule-web", "rails_web"), ("api-geteway", "hanami_api"), ("ops-console", "ops_service")):
                match = re.search(r"upstream " + upstream + r" \{.*?\n\}", text, re.S)
                if match:
                    servers = re.findall(r"server ([0-9.]+):([0-9]+)(?![0-9])", match[0])
                    if not healthy[service] or any((ip, int(port)) not in healthy[service] for ip, port in servers if ip != "127.0.0.1"):
                        text = text.replace(match[0], f"upstream {upstream} {{ server 127.0.0.1:9 down; }}")
        import re
        scrubbed = re.sub(r"upstream (rails_web|hanami_api|ops_service) \{", "", text)
        scrubbed = re.sub(r"zone (rails_web|hanami_api|ops_service) 64k;|keepalive (8|16);|server [0-9.]+:[0-9]+(?: max_fails=2 fail_timeout=5s| down)?;|\}", "", scrubbed)
        if scrubbed.strip():
            text = fallback
        if text != applied:
            previous = active.read_text()
            active.write_text(text)
            if subprocess.run(["nginx", "-t"], capture_output=True).returncode == 0:
                nginx.send_signal(signal.SIGHUP)
                applied = text
            else:
                active.write_text(previous)
                print("Rejected invalid Nginx candidate", flush=True)
finally:
    if registration:
        registration.set()
    ct.terminate()
    nginx.send_signal(signal.SIGQUIT)
    for child in (ct, nginx):
        try:
            child.wait(timeout=10)
        except subprocess.TimeoutExpired:
            child.kill()
