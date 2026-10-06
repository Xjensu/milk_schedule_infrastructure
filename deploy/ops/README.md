# Hanami operations console

Follow the [deployment guide](../DEPLOYMENT_GUIDE.md) first. Nginx serves `/ops/` only to the administrator client networks configured in `.env.local` through `ADMIN_LAN_CIDRS`.

`deploy/bin/init-env.py` creates the private `deploy/ops/.env.local` once. Edit `OPS_CONSOLE_USERNAME` and `OPS_CONSOLE_PASSWORD` there. These credentials are separate from the application administrator and PostgreSQL account. The console runs the same release image as the API.

The console is unprivileged, uses a read-only root filesystem and permits only `hanami db version`, `create`, `migrate`, `prepare` and `seed`. It has no arbitrary shell, environment editor, database-drop control or Docker socket. The current HTTP ingress does not encrypt Basic Authentication; use a trusted encrypted network until HTTPS is configured.

After changing console credentials:

```sh
./deploy/bin/compose.sh up -d --no-build ops_console
```

The deployment script runs `db migrate` before starting application services. Seed a new installation using the deployment guide or the console. Seeding requires `SEED_ADMIN_PASSWORD` from the root `.env.local` and does not reset an existing administrator.

For status/logs, use `deploy/bin/compose.sh` over SSH. A restart alone does not apply changed environment values. Never print or share the private environment files.

Hanami `db prepare` also runs seeds. Use `deploy/bin/db.sh migrate` for routine schema updates and `deploy/bin/db.sh seed` for intentional seeding.
