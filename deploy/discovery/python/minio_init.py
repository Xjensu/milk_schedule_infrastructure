"""Initialize private buckets through discovery without exposing credentials in argv."""
import os
import subprocess
from urllib.parse import quote, urlsplit
from discovery import endpoint, start_registration, wait_for

wait_for("minio")
stop = start_registration(lambda: True)
try:
    address = urlsplit(endpoint("minio"))
    environment = os.environ.copy()
    environment["MC_HOST_local"] = (f"http://{quote(environment['MINIO_ACCESS_KEY'], safe='')}:"
                                     f"{quote(environment['MINIO_SECRET_KEY'], safe='')}@{address.netloc}")
    for key, default in (("MINIO_BUCKET", "excel-files"), ("MEDIA_QUARANTINE_BUCKET", "media-quarantine"),
                         ("MEDIA_CLEAN_BUCKET", "media-clean"), ("NOTICE_EXPORT_BUCKET", "milk-schedule-notices")):
        target = "local/" + environment.get(key, default)
        for args in (["mb", "--ignore-existing", target], ["anonymous", "set", "none", target]):
            result = subprocess.run(["mc", *args], env=environment, capture_output=True)
            if result.returncode:
                raise SystemExit("Private bucket initialization failed")
    print("Private storage buckets ready")
finally:
    if stop:
        stop.set()
