# Build and publish images to Docker Hub

The published release `2026-10-06-1` includes all seven default application images for `linux/amd64`. Its verified Docker Hub digests are recorded in [the release manifest](image-releases/2026-10-06-1.json).

Run image builds and pushes on the development PC. The deployment server pulls the published images. Publishing images does not start/restart the development application or deploy anything to the server.

## 1. Prepare the build workspace

The build root needs `compose.build.yml`, `deploy/`, and compatible application sources at these paths:

```
apps/schedule_web
apps/api_geteway
apps/excel_processor
apps/scheduler
```

The infrastructure repository alone does not include those application sources. Use the complete development workspace or place the compatible source checkouts at the expected paths in an infrastructure checkout. `apps/frontend` is needed only for the optional legacy frontend build.

Install Docker with the Compose plugin and Buildx. Run shell commands through Bash/WSL when using Windows. Verify Docker access:

```bash
docker version
docker compose version
docker buildx version
```

Build for the deployment server's architecture. Linux amd64 is the verified target. If the build machine differs from an amd64 server, set `export DOCKER_DEFAULT_PLATFORM=linux/amd64` before building. ARM compatibility of the pinned dependencies has not been verified.

Commit application changes in their owning Git repositories when preparing a reproducible release. Building from a dirty worktree includes those uncommitted source changes in the image.

## 2. Authenticate to Docker Hub

Create/use the `xjensu` account and the required repositories. Choose their public/private visibility deliberately. Generate a personal access token with permission to push to the intended repositories, then log in:

```bash
docker login --username xjensu
```

Enter the token at the prompt. Do not put it in `.env`, source files, Git commits or a `--password TOKEN` argument. Automated workflows should supply a protected secret through `--password-stdin`; see [Docker login documentation](https://docs.docker.com/reference/cli/docker/login/).

A deployment server pulling private repositories needs its own Docker login with pull access. It does not need the build machine's push token.

## 3. Configure registry names and choose a tag

From the build workspace root:

```bash
[ -f .env ] || cp .env.compose.example .env
nano .env
```

Set `IMAGE_NAMESPACE=xjensu`. The build script reads this development `.env`; the server reads its own `.env.local`. Server passwords and host addresses are not needed for builds.

Choose a new tag for each release, for example `2026-10-06-1`, then `2026-10-06-2`. Treat a tag already deployed as immutable. Publishing a new release does not require overwriting an old tag or `latest`.

| Repository | Build service | Purpose |
| --- | --- | --- |
| `xjensu/table-bsut-by` | `schedule_web` | Rails web interface |
| `xjensu/table-api` | `api_geteway` | API, operations console and API workers |
| `xjensu/excel-processor` | `excel_processor` | Excel worker |
| `xjensu/table-scheduler` | `scheduler` | Scheduling solver |
| `xjensu/table-discovery` | `discovery_acl` | Registrars and ACL initializer |
| `xjensu/table-minio-init` | `minio_init` | Private bucket initializer |
| `xjensu/table-edge` | `nginx` | Nginx ingress |

Workers share the API image, and registrars share the discovery image; they do not need separate pushes. PostgreSQL, Redis, MinIO and Consul use upstream images and are not built or republished by this project.

## 4. Build and push the required images

Recommended command on the development PC:

```bash
./deploy/bin/build-images.sh 2026-10-06-1 --push
```

The script validates the build configuration, builds all seven required custom images and pushes them under the same tag. Docker tags each build from its Compose `image:` setting; see [Compose build](https://docs.docker.com/reference/cli/docker/compose/build/) and [Compose push](https://docs.docker.com/reference/cli/docker/compose/push/).

To build first and inspect before publishing:

```bash
./deploy/bin/build-images.sh 2026-10-06-1

IMAGE_TAG=2026-10-06-1 docker compose --env-file .env \
  -f compose.build.yml config --images

IMAGE_TAG=2026-10-06-1 docker compose --env-file .env \
  -f compose.build.yml push
```

Application Docker build contexts exclude local `.env` files, Git metadata, private keys and assistant tooling. Keep those exclusions intact. Do not pass production secrets as build arguments or add private runtime configuration to Dockerfiles.

The running development containers remain on their existing image IDs; rebuilding/pushing images does not recreate them.

## 5. Push or retry individual images

After building the tag, individual commands are:

```bash
docker push xjensu/table-bsut-by:2026-10-06-1
docker push xjensu/table-api:2026-10-06-1
docker push xjensu/excel-processor:2026-10-06-1
docker push xjensu/table-scheduler:2026-10-06-1
docker push xjensu/table-discovery:2026-10-06-1
docker push xjensu/table-minio-init:2026-10-06-1
docker push xjensu/table-edge:2026-10-06-1
```

A partially completed upload does not require rebuilding. Retry the push for the same unchanged local image/tag; Docker reuses layers already uploaded. Do not switch a server to a release until all seven required tags are present.

If reusing an existing local image intentionally, tag it first:

```bash
docker tag xjensu/table-bsut-by:local xjensu/table-bsut-by:2026-10-06-2
docker push xjensu/table-bsut-by:2026-10-06-2
```

Retagging does not rebuild source or assets. Use it only when the existing image is the release you intend to publish.

## 6. Verify the registry after pushing

Inspect manifests from Docker Hub rather than relying only on local image listings:

```bash
docker buildx imagetools inspect xjensu/table-bsut-by:2026-10-06-1
docker buildx imagetools inspect xjensu/table-api:2026-10-06-1
docker buildx imagetools inspect xjensu/excel-processor:2026-10-06-1
docker buildx imagetools inspect xjensu/table-scheduler:2026-10-06-1
docker buildx imagetools inspect xjensu/table-discovery:2026-10-06-1
docker buildx imagetools inspect xjensu/table-minio-init:2026-10-06-1
docker buildx imagetools inspect xjensu/table-edge:2026-10-06-1
```

Each must return a manifest/digest and the expected platform. Keep the matching infrastructure Git revision and image tag together. A successful push proves publication; it does not replace application validation.

## 7. Optional images

Publish Fluentd if enabling monitoring for the release:

```bash
IMAGE_TAG=2026-10-06-1 docker compose --env-file .env \
  -f compose.build.yml --profile observability build --pull fluentd
IMAGE_TAG=2026-10-06-1 docker compose --env-file .env \
  -f compose.build.yml --profile observability push fluentd
```

Publish the legacy frontend only if that profile is used:

```bash
IMAGE_TAG=2026-10-06-1 docker compose --env-file .env \
  -f compose.build.yml --profile legacy-frontend build --pull frontend
IMAGE_TAG=2026-10-06-1 docker compose --env-file .env \
  -f compose.build.yml --profile legacy-frontend push frontend
```

These produce `xjensu/table-fluentd:2026-10-06-1` and `xjensu/table-frontend:2026-10-06-1`. Neither is required by the default deployment.

## 8. Use the release on the separate server

Follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for first installation, database setup and backups. On an existing server, update the compatible infrastructure checkout, edit `.env.local` and select:

```dotenv
IMAGE_NAMESPACE=xjensu
IMAGE_TAG=2026-10-06-1
```

Then run the deployment wrapper, which pulls images and applies migrations:

```bash
./deploy/bin/deploy-discovery.sh
```

No host IP entry or server image build is required. Publishing to Docker Hub alone does not deploy the application. Back up before schema-changing updates.

## Troubleshooting

| Error | Action |
| --- | --- |
| Authentication required / denied | Log in to the intended account; check token permissions and repository namespace. |
| Local tag does not exist | Build the exact tag or deliberately retag the intended existing image. |
| Build context is missing | Supply compatible application sources in the development workspace; the infrastructure-only server checkout is not a full build workspace. |
| Network interruption during push | Retry the same push; already uploaded layers are reused. |
| Server cannot find a tag | Verify all seven remote manifests; confirm `.env.local` uses the same namespace/tag. |
| `exec format error` on server | Build for the server architecture. |
| Optional profile image missing | Build/push its service explicitly before enabling that profile. |

Official reference: [Push images to Docker Hub](https://docs.docker.com/docker-hub/repos/manage/hub-images/push/).
