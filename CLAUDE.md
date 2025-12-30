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

### GitLab (Source Control & CI/CD)
- **Config:** `infrastructure/gitlab/docker-compose.yml`
- **URL:** http://10.0.0.84:8090
- **Registry:** http://10.0.0.84:5050
- **SSH Port:** 2222
- **Docs:** `docs/GITLAB_DEPLOYMENT.md`

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
docker logs gitlab -f --tail 100
```

### Deploy GitLab Changes
```bash
cd /opt/wizardsofts-megabuild/infrastructure/gitlab
docker-compose down && docker-compose up -d
```

### Check GitLab Health
```bash
docker ps | grep gitlab  # Look for (healthy) status
docker exec gitlab gitlab-ctl status  # Check internal services
curl http://10.0.0.84:8090/-/readiness  # Check readiness endpoint
```

## Recent Changes (2025-12-30/31)

### GitLab Health Check Fixed (2025-12-31)
- **Issue:** GitLab container showing "unhealthy" with 1500+ failing streak
- **Root Cause:** Health check was using `http://localhost/-/health` (port 80) but GitLab is configured to listen on port 8090
- **Fix:** Updated health check to `http://localhost:8090/-/health`
- **Lesson Learned:** When using non-standard ports in `external_url`, ensure health checks match the configured port

### Appwrite Deployment Fixed (2025-12-30)
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

1. Check Serena memories: `appwrite-deployment-troubleshooting`, `traefik-*`, `gitlab-*`
2. Review docs in `/docs/` directory
3. Check container logs with `docker logs <container-name>`

### GitLab Troubleshooting

**Container shows "unhealthy":**
1. Check health check output: `docker inspect --format='{{json .State.Health}}' gitlab`
2. Verify the health check port matches `external_url` in GITLAB_OMNIBUS_CONFIG
3. Check internal services: `docker exec gitlab gitlab-ctl status`
4. Review logs: `docker logs gitlab --tail 200`

**GitLab not accessible:**
1. Verify ports are exposed: `docker ps | grep gitlab`
2. Check nginx inside container: `docker exec gitlab gitlab-ctl status nginx`
3. Test from server: `curl http://localhost:8090/-/readiness`

**Database connection issues:**
1. Verify PostgreSQL is running: `docker ps | grep postgres`
2. Check GitLab can reach DB: `docker exec gitlab gitlab-rake gitlab:check`
