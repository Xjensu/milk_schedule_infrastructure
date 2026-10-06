FROM quay.io/minio/mc@sha256:a7fe349ef4bd8521fb8497f55c6042871b2ae640607cf99d9bede5e9bdf11727 AS client
FROM python:3.11.11-slim-bookworm@sha256:081075da77b2b55c23c088251026fb69a7b2bf92471e491ff5fd75c192fd38e5
COPY --from=client /usr/bin/mc /usr/local/bin/mc
COPY python/ /opt/discovery/python/
ENV PYTHONPATH=/opt/discovery/python PYTHONDONTWRITEBYTECODE=1
ENTRYPOINT ["python", "/opt/discovery/python/minio_init.py"]
