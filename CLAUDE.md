# WizardSofts Megabuild - Claude Code Instructions

## Project Overview

This is a monorepo containing multiple WizardSofts applications and shared infrastructure:

- **Backend Services:** Java Spring microservices (ws-gateway, ws-discovery, ws-company, ws-trades, ws-news)
- **Frontend Apps:** React/Next.js applications (gibd-quant-web, gibd-news, ws-wizardsofts-web, etc.)
- **Infrastructure:** Docker Compose configurations for Appwrite, Traefik, monitoring

## Key Directories

- `/apps/` - Application code (each app has its own CLAUDE.md)
- `/docker-compose.*.yml` - Service orchestration files
- `/traefik/` - Traefik reverse proxy configuration
- `/docs/` - Deployment guides and documentation

## Infrastructure Components

### Appwrite (BaaS)
- **Config:** `docker-compose.appwrite.yml`
- **Env:** `.env.appwrite`
- **Domain:** appwrite.wizardsofts.com
- **Docs:** `docs/APPWRITE_DEPLOYMENT.md`
- **Memory:** `appwrite-deployment-troubleshooting`

### Traefik (Reverse Proxy)
- **Config:** `traefik/traefik.yml`, `traefik/dynamic/`
- **Memories:** `traefik-configuration-guide`, `traefik-network-requirements`, `https-dns-strategy`

## Server Infrastructure

| Server | IP | Purpose |
|--------|-----|---------|
| HP Server | 10.0.0.84 | Production (Appwrite, microservices) |
| Hetzner | 178.63.44.221 | External services |

## Common Tasks

### Deploy Appwrite Changes
```bash
cd /opt/wizardsofts-megabuild
docker-compose -f docker-compose.appwrite.yml --env-file .env.appwrite down
docker-compose -f docker-compose.appwrite.yml --env-file .env.appwrite up -d
```

### Check Service Health
```bash
docker-compose -f docker-compose.appwrite.yml ps
curl https://appwrite.wizardsofts.com/v1/health
```

### View Logs
```bash
docker logs appwrite -f --tail 100
docker logs traefik -f --tail 100
```

## Recent Changes (2025-12-30)

### Appwrite Deployment Fixed
- Fixed invalid entrypoints (schedule -> schedule-functions, etc.)
- Added missing `_APP_DOMAIN_TARGET_CNAME` environment variable
- Removed restrictive container security settings causing permission errors
- Enabled signup whitelist to block public registration

## Git Workflow

- Main branch: `master`
- Always commit with descriptive messages
- Update docs and memories after significant infrastructure changes

## Credentials

Stored in `.env.appwrite` (not in git). Key variables:
- `_APP_OPENSSL_KEY_V1`
- `_APP_SECRET`
- `_APP_DB_PASS`
- `_APP_EXECUTOR_SECRET`

## Troubleshooting

1. Check Serena memories: `appwrite-deployment-troubleshooting`, `traefik-*`
2. Review docs in `/docs/` directory
3. Check container logs with `docker logs <container-name>`
