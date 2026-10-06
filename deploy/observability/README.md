# Optional monitoring

This overlay runs Prometheus, Loki, Fluentd and Grafana. The server pulls `xjensu/table-fluentd:IMAGE_TAG`; build/push it on the workstation using the instructions in the [deployment guide](../DEPLOYMENT_GUIDE.md).

`deploy/bin/init-env.py` creates `deploy/observability/.env.local` with private Grafana credentials. Existing files are preserved. The password initializes a new Grafana volume only; later changes require Grafana's own password change/reset procedure.

From the server deployment directory:

```sh
./deploy/bin/compose.sh -f deploy/observability/docker-compose.observability.yml \
  --profile observability config --quiet
./deploy/bin/compose.sh -f deploy/observability/docker-compose.observability.yml \
  --profile observability pull prometheus loki fluentd grafana
./deploy/bin/compose.sh -f deploy/observability/docker-compose.observability.yml \
  --profile observability up -d --no-build prometheus loki fluentd grafana
```

Prometheus joins the private discovery network and resolves the Rails replicas through Docker DNS to scrape `/metrics`. Grafana provisions the existing data sources and dashboard. The scrape failure and circuit-breaker alert rules remain active.

Host ports bind to loopback: Grafana 3001, Prometheus 9090, Loki 3100, Fluent Forward 24224. Use SSH tunnels for access:

```sh
ssh -L 3001:127.0.0.1:3001 -L 9090:127.0.0.1:9090 deploy@SERVER
```

Open `http://127.0.0.1:3001` on your PC. Fluentd mounts `/var/lib/docker/containers` read-only and assumes the Docker JSON-file log layout used by this stack. It does not mount the Docker socket.

Stop only monitoring without stopping the application:

```sh
./deploy/bin/compose.sh -f deploy/observability/docker-compose.observability.yml \
  --profile observability stop prometheus loki fluentd grafana
```

Do not use `down` on the merged configuration to stop only monitoring: it also includes the main application's services. Named volumes retain history and Grafana state.
