"""Third-party service registrar, running in the target container's network namespace."""
import os
import signal
import socket
from urllib.request import build_opener, ProxyHandler
from discovery import register
import threading

stop = threading.Event()
for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, lambda *_: stop.set())
opener = build_opener(ProxyHandler({}))


def healthy():
    try:
        path = os.environ.get("DISCOVERY_HEALTH_PATH")
        port = int(os.environ["DISCOVERY_PORT"])
        if path:
            with opener.open(f"http://127.0.0.1:{port}{path}", timeout=2) as response:
                return response.status == 200
        with socket.create_connection(("127.0.0.1", port), timeout=2):
            return True
    except Exception:
        return False


register(stop, healthy)
