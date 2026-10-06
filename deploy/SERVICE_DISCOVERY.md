# Discovery deployment and ingress

## Architecture

The supported deployment is one Linux Docker host. `docker-compose.yml` runs a persistent Consul server, two Rails/Falcon containers, and Nginx. The separate frontend is retained behind the optional `legacy-frontend` profile on loopback port 8080; it is not the active website.

Ruby and Python applications query Consul's passing health entries. Internal IP addresses and ports belong to discovery. Credentials, database/bucket names, Redis database numbers, and tuning remain protected configuration. Browser-facing signed download URLs are an external address, not a discoverable container address.

Applications register unique container identities and refresh their TTL checks every five seconds. Third-party services have unprivileged companion registrars sharing their network namespace. Those companions have no Docker socket. Workers report recent queue-loop progress; the bounded 1,200-second processing allowance accommodates long solver/sanitizer batches. PostgreSQL and Redis registrar checks are TCP liveness; application readiness separately verifies authenticated access.

Consul uses persisted storage, default-deny ACLs, and separate tokens scoped to each service and its dependencies. The server's management token is private to the server and the one-shot policy provisioner. The Consul UI and API have no published host port. It is not a secret store or a high-availability deployment.

## First deployment

Keep the existing `.env.local` and `deploy/ops/.env.local` private. Required values include PostgreSQL credentials and database name, Redis password, application signing keys, MinIO credentials and bucket names, and operations-console credentials. Never print these files or a fully interpolated Compose model.

After cloning the main repository from GitHub and configuring `.env.local`, run:

```sh
deploy/bin/deploy-discovery.sh
```

The preflight automatically selects a single private IPv4 LAN interface, excluding loopback, container bridges, and recognizable tunnel interfaces. For an ambiguous server:

```sh
ADMIN_INTERFACE=enp1s0 ADMIN_LAN_CIDRS=192.168.10.0/24 deploy/bin/deploy-discovery.sh
```

The standard router-forwarding setup requires no host IP in `.env.local`: Nginx listens on all host interfaces at port 80. Automatic detection selects a private IPv4 address, preferring the normal outbound route when multiple LAN interfaces exist. Set `LAN_BIND_IP` in `.env.local` to explicitly select another assigned address, including a public address; a public address requires explicit trusted client `ADMIN_LAN_CIDRS`. Prefer a private/VPN interface for administration. Never use `0.0.0.0/0`; this deployment supports IPv4 administrator CIDRs only. The allowlist describes clients, not the server address.

Generated network policy, token files, and Consul server configuration live in ignored `deploy/generated/`. Keep this directory private and back up its credentials with Consul's data. Do not copy a generated host policy to another server: run the preflight there. Detection runs only at deployment; a later network change does not silently change the allowlist. Use the selected LAN address for host-local administration too, because Docker may translate loopback connections to a bridge peer address.

All subsequent Compose commands must use the generated environment:

```sh
./deploy/bin/compose.sh config --quiet
./deploy/bin/compose.sh ps
```

## Access and ports

| Destination | Access |
| --- | --- |
| Nginx TCP 80 | Public IPv4, subject to denylist and rate limits |
| `/admin`, `/cabinet`, `/session`, `/password`, `/consent` | Detected/explicit LAN only |
| `/ops`, health, metrics, administrative/authentication API routes | LAN only; application authentication still applies |
| Internal generation callbacks | Never browser-accessible through Nginx |
| MinIO TCP 9000 | Selected LAN address, source-CIDR firewall enforced |
| Rails, API, PostgreSQL, Redis, scheduler, Consul, workers, MinIO console | Unpublished Docker-internal ports |

Nginx discards supplied forwarding headers and passes its direct peer address. Rails and Hanami trust only the fixed Nginx address on the private discovery network. If a CDN, reverse proxy, or source-NAT router hides real client addresses, do not broadly trust its headers or LAN address: configure a specific trusted-proxy policy before exposure.

HTTP is unencrypted. Public users can read schedules; all account use stays on the trusted LAN. LAN restrictions do not encrypt passwords or cookies. TLS and public authenticated access are not provided by this deployment.

The firewall installer owns `MILK_INGRESS` in Docker's `DOCKER-USER` path and `MILK_HOST` for the selected host address on TCP 9000 in `INPUT`. Both Docker DNAT and userland-proxy paths are covered. It preserves SSH and unrelated services. It requires Docker's iptables backend (iptables-nft is supported). It uses root/passwordless sudo if available, otherwise an ephemeral `NET_ADMIN` Docker helper; application containers are not privileged. Run it after container replacement and after host/firewall restarts:

```sh
python3 deploy/bin/install-project-firewall.py
```

The deployment wrapper pulls prebuilt images, prepares the database and runs this step automatically. It never builds on the server. See [the deployment guide](DEPLOYMENT_GUIDE.md) for building and packaging releases. If it fails, the deployment is not ready for public exposure. Router forwarding, external firewall policy, and proving reachability from another physical network remain server-operator responsibilities.

## Limits and blocking

Nginx's shared counters enforce a general 20 requests/second per IP with burst 100; authentication writes use 10/minute with burst 5; operations use 6/minute with burst 4. Concurrent requests are capped at 50/IP. Fingerprinted assets are excluded from the general request-rate budget. Application limits remain active and may be stricter, especially for visitors sharing one school NAT address. Rejections return 429 and a Russian response.

Maintain `deploy/edge/denylist.geo` with entries such as `198.51.100.23/32 1;`, then validate and reload:

```sh
./deploy/bin/compose.sh exec nginx nginx -t
./deploy/bin/compose.sh exec nginx nginx -s reload
```

There are no automatic permanent or temporary IP bans. Nginx logs omit query strings, cookies, authorization headers, request bodies, and signed download capabilities.

## Failure behavior and maintenance

Runtime clients refresh discovery results every five seconds. Transport failures permit a last verified nonempty result for at most 60 seconds. A successful empty result immediately means unavailable. Processes without cached endpoints wait up to 120 seconds at startup, then exit so Compose can restart them. Nginx validates generated upstreams before graceful reload and serves 503 when no healthy endpoints exist or its discovery verification expires.

Existing database transactions keep their checked-out connection; idle connections are drained on an endpoint change. Redis, storage, and HTTP clients resolve updated endpoints. No new transport retry replays writes. Excel's existing Redis Pub/Sub delivery semantics are retained; this migration does not add guaranteed message delivery.

Only graceful exits can immediately deregister; crashes become critical through TTL expiry and disappear after two minutes. Consul recovery triggers re-registration. There is one registry, one host, and one instance of each stateful dependency, so two Rails replicas provide web-process redundancy rather than complete system availability.

For existing schema maintenance, use the established operations console or:

```sh
./deploy/bin/db.sh migrate
```

Never reset volumes or use `down -v`. To roll back, restore the prior deployment repository revision and its compatible image tag, then start them with their original configuration. Preserve database, MinIO, Redis, and Consul data; remove only attributable ingress firewall rules if reverting their policy. Back up before changes requiring schema rollback.

Record actual runtime acceptance separately; syntax success does not prove a functioning administrator journey or an externally verified LAN boundary.
