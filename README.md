# Milk Schedule

Current release: **2026-10-21-1**. All deployment instructions are in [one deployment guide](deploy/DEPLOYMENT_GUIDE.md).

The application uses a Rails web interface, a Hanami API, Python Excel and scheduling workers, PostgreSQL, Redis, MinIO and Nginx with Compose DNS.

Build custom images on a workstation, push them to Docker Hub, then run the server from those images. The server needs Docker, the Compose plugin, Python 3 and a clone of this main repository; it does not need application source, Ruby, Node.js or a compiler.

- [Deployment guide](deploy/DEPLOYMENT_GUIDE.md): installation from zero, administrator setup, updates, Consul migration, automatic recovery, antivirus, diagnostics and rollback.
- [Optional monitoring](deploy/observability/README.md).
- [Database operations console](deploy/ops/README.md).

`docker-compose.yml` is image-only. `compose.build.yml` is a separate workstation build definition. On the server, clone this main repository, generate/edit `.env.local`, pull the images and run Hanami migrations. Host networking is detected automatically. The archive packaging script is optional; keep the deployment repository revision compatible with the image tag.

Application sources under `apps/` include independent Git repositories. A root checkout alone does not supply all application sources; builds use the compatible application checkouts already present on the workstation. Commit application changes in their owning repositories before publishing a reproducible release. Product requirements and design records remain in `docs/`.
