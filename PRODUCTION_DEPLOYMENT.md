# Production Deployment to 10.0.0.84

**Last Updated**: December 27, 2025

---

## 🚀 Quick Deployment

### Prerequisites

1. **SSH Access**: Ensure SSH key is added to server
2. **Server Access**: Can reach 10.0.0.84 from your network
3. **Docker**: Docker and Docker Compose installed on server

---

## Option 1: Automated Deployment (Recommended)

### Setup SSH Access First

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t rsa -b 4096

# Copy SSH key to server
ssh-copy-id deploy@10.0.0.84

# Test connection
ssh deploy@10.0.0.84 "echo 'Connected successfully'"
```

### Run Deployment Script

```bash
cd /Users/mashfiqurrahman/Workspace/wizardsofts-megabuild

# Deploy everything (all services)
./scripts/deploy-to-84.sh
```

---

## Option 2: Manual Deployment

### Step 1: Copy Files to Server

```bash
# From your local machine
cd /Users/mashfiqurrahman/Workspace/wizardsofts-megabuild

rsync -avz --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude 'target' \
    --exclude '.m2' \
    --exclude '.cache' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --progress \
    ./ deploy@10.0.0.84:/opt/wizardsofts-megabuild/
```

### Step 2: SSH to Server

```bash
ssh deploy@10.0.0.84
```

### Step 3: Deploy on Server

```bash
cd /opt/wizardsofts-megabuild

# Create .env file (if doesn't exist)
if [ ! -f .env ]; then
    cp .env.example .env
    nano .env  # Edit with actual values
fi

# Stop existing services
docker compose down

# Build all images
docker compose --profile all build

# Start all services
docker compose --profile all up -d

# Check status
docker compose ps
```

---

## 🌐 Production URLs

### Web Applications

| Application | URL | Description |
|-------------|-----|-------------|
| **Wizardsofts.com** | http://10.0.0.84:3000 | Corporate website |
| **Daily Deen Guide** | http://10.0.0.84:3002 | Islamic prayer times |
| **GIBD Quant-Flow** | http://10.0.0.84:3001 | Stock trading signals |

### Infrastructure Services

| Service | URL | Description |
|---------|-----|-------------|
| **Eureka Dashboard** | http://10.0.0.84:8762 | Service registry |
| **API Gateway** | http://10.0.0.84:8080 | Gateway routes |

### Python ML Services

| Service | URL | Description |
|---------|-----|-------------|
| **Signal Service** | http://10.0.0.84:5001 | Generate trading signals |
| **NLQ Service** | http://10.0.0.84:5002 | Natural language queries |
| **Calibration Service** | http://10.0.0.84:5003 | Stock calibration |
| **Agent Service** | http://10.0.0.84:5004 | AI agents |

### Spring Boot APIs

| Service | URL | Description |
|---------|-----|-------------|
| **Trades API** | http://10.0.0.84:8182 | OHLCV trade data |
| **Company API** | http://10.0.0.84:8183 | Company information |
| **News API** | http://10.0.0.84:8184 | Market news |

---

## 🌍 Domain-Based URLs (With DNS)

Once DNS is configured, services will be available at:

### Public Web Applications

| Domain | IP | Port | Description |
|--------|-----|------|-------------|
| **www.wizardsofts.com** | 10.0.0.84 | 443 (HTTPS) | Corporate website |
| **dailydeenguide.wizardsofts.com** | 10.0.0.84 | 443 (HTTPS) | Daily Deen Guide |
| **quant.wizardsofts.com** | 10.0.0.84 | 443 (HTTPS) | Quant-Flow |

### Infrastructure Services

| Domain | IP | Description |
|--------|-----|-------------|
| **traefik.wizardsofts.com** | 10.0.0.84 | Traefik dashboard |
| **id.wizardsofts.com** | 10.0.0.84 | Keycloak (auth) |
| **gitlab.wizardsofts.com** | 10.0.0.84 | GitLab CI/CD |
| **nexus.wizardsofts.com** | 10.0.0.84 | Artifact repository |
| **grafana.wizardsofts.com** | 10.0.0.84 | Monitoring dashboard |
| **n8n.wizardsofts.com** | 10.0.0.84 | Workflow automation |
| **mail.wizardsofts.com** | 10.0.0.84 | Mailcow (email) |

---

## 📋 DNS Configuration Needed

### A Records

```
# Web Applications
www.wizardsofts.com             A    10.0.0.84
dailydeenguide.wizardsofts.com  A    10.0.0.84
quant.wizardsofts.com           A    10.0.0.84

# Infrastructure Services
traefik.wizardsofts.com         A    10.0.0.84
id.wizardsofts.com              A    10.0.0.84
gitlab.wizardsofts.com          A    10.0.0.84
nexus.wizardsofts.com           A    10.0.0.84
grafana.wizardsofts.com         A    10.0.0.84
n8n.wizardsofts.com             A    10.0.0.84
mail.wizardsofts.com            A    10.0.0.84

# VPN Server (Dynamic DNS)
vpn.wizardsofts.com             A    <updated by update_dns script>
```

### MX Records (for Mailcow)

```
@    MX    10    mail.wizardsofts.com
```

### TXT Records (SPF, DMARC)

```
@         TXT    "v=spf1 mx ~all"
_dmarc    TXT    "v=DMARC1; p=quarantine; rua=mailto:postmaster@wizardsofts.com"
```

---

## ✅ Health Checks

### Quick Test Script

```bash
#!/bin/bash

HOST="10.0.0.84"

echo "Testing production services on $HOST..."
echo ""

# Web Apps
echo "=== Web Applications ==="
curl -I http://$HOST:3000 2>&1 | head -1  # Wizardsofts.com
curl -I http://$HOST:3002 2>&1 | head -1  # Daily Deen Guide
curl -I http://$HOST:3001 2>&1 | head -1  # Quant-Flow

# Infrastructure
echo ""
echo "=== Infrastructure Services ==="
curl -s http://$HOST:8762/actuator/health  # Eureka
curl -s http://$HOST:8080/actuator/health  # Gateway

# ML Services
echo ""
echo "=== Python ML Services ==="
curl -s http://$HOST:5001/health  # Signal
curl -s http://$HOST:5002/health  # NLQ
curl -s http://$HOST:5003/health  # Calibration
curl -s http://$HOST:5004/health  # Agent

# Spring Boot APIs
echo ""
echo "=== Spring Boot APIs ==="
curl -s http://$HOST:8182/actuator/health  # Trades
curl -s http://$HOST:8183/actuator/health  # Company
curl -s http://$HOST:8184/actuator/health  # News
```

### Individual Service Checks

```bash
# From your local machine or any machine that can access 10.0.0.84

# Test Wizardsofts.com
curl http://10.0.0.84:3000

# Test Daily Deen Guide
curl http://10.0.0.84:3002

# Test Quant-Flow
curl http://10.0.0.84:3001

# Test Eureka (should show registered services)
curl http://10.0.0.84:8762/eureka/apps

# Test Gateway health
curl http://10.0.0.84:8080/actuator/health

# Test Signal Service
curl -X POST http://10.0.0.84:5001/api/v1/signals/generate \
  -H "Content-Type: application/json" \
  -d '{"ticker": "GP"}'
```

---

## 🔧 Server Configuration

### Environment Variables (.env)

SSH to the server and edit `.env`:

```bash
ssh deploy@10.0.0.84
cd /opt/wizardsofts-megabuild
nano .env
```

**Required Variables**:

```bash
# Database
DB_PASSWORD=your_secure_password_here

# OpenAI (for NLQ and Agent services)
OPENAI_API_KEY=sk-your-actual-api-key

# Optional: Analytics
GA_MEASUREMENT_ID=G-XXXXXXXXXX
ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXXXXXXXX

# Infrastructure (if using infrastructure services)
KEYCLOAK_DB_PASSWORD=keycloak_db_password
KEYCLOAK_ADMIN_PASSWORD=secure_password
TRAEFIK_DASHBOARD_PASSWORD=secure_password
N8N_PASSWORD=secure_password
GRAFANA_PASSWORD=secure_password
GITLAB_ROOT_PASSWORD=secure_password
INFRA_DB_PASSWORD=secure_password
NEXUS_ADMIN_PASSWORD=secure_password
```

---

## 🚀 Deployment Profiles

You can deploy specific subsets of services using profiles:

### Deploy Only Web Apps

```bash
docker compose --profile web-apps up -d
```

**Services**: Wizardsofts.com, Daily Deen Guide

---

### Deploy Only GIBD Quant-Flow

```bash
docker compose --profile gibd-quant up -d
```

**Services**: All ML services + Quant-Flow frontend + shared infrastructure

---

### Deploy Shared Services Only

```bash
docker compose --profile shared up -d
```

**Services**: Postgres, Redis, Eureka, Gateway, Spring Boot APIs

---

### Deploy Everything

```bash
docker compose --profile all up -d
```

**Services**: All of the above

---

## 📊 Monitoring

### View Service Status

```bash
ssh deploy@10.0.0.84
cd /opt/wizardsofts-megabuild

# List all running containers
docker compose ps

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f ws-wizardsofts-web
docker compose logs -f gibd-quant-signal

# Check resource usage
docker stats
```

### Check Eureka Registration

```bash
# View all registered services
curl http://10.0.0.84:8762/eureka/apps | grep -o '<app>[^<]*</app>'

# Expected services:
# - WS-DISCOVERY
# - WS-GATEWAY
# - WS-TRADES
# - WS-COMPANY
# - WS-NEWS
# - GIBD-QUANT-SIGNAL
# - GIBD-QUANT-NLQ
# - GIBD-QUANT-CALIBRATION
# - GIBD-QUANT-AGENT
```

---

## 🔄 Update Deployment

### Pull Latest Changes

```bash
ssh deploy@10.0.0.84
cd /opt/wizardsofts-megabuild

# Option 1: If using git
git pull origin main

# Option 2: Rsync from local (from your machine)
rsync -avz --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude 'target' \
    ./ deploy@10.0.0.84:/opt/wizardsofts-megabuild/
```

### Rebuild and Restart

```bash
ssh deploy@10.0.0.84
cd /opt/wizardsofts-megabuild

# Rebuild changed services
docker compose --profile all build

# Restart all services
docker compose --profile all up -d

# Or restart specific service
docker compose restart ws-wizardsofts-web
```

---

## 🔥 Troubleshooting

### Service Won't Start

```bash
# Check logs
docker compose logs <service-name>

# Check if port is already in use
ss -tulpn | grep <port>

# Restart service
docker compose restart <service-name>

# Remove and recreate
docker compose rm -f <service-name>
docker compose up -d <service-name>
```

### Out of Disk Space

```bash
# Clean up Docker
docker system prune -a --volumes -f

# Check disk usage
df -h
```

### Cannot Access Services from Outside

```bash
# Check firewall
sudo ufw status

# Allow ports
sudo ufw allow 3000/tcp  # Wizardsofts.com
sudo ufw allow 3001/tcp  # Quant-Flow
sudo ufw allow 3002/tcp  # Daily Deen Guide
sudo ufw allow 8080/tcp  # Gateway
sudo ufw allow 8762/tcp  # Eureka

# Or use Traefik (ports 80/443)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## 📝 Next Steps

1. ✅ Deploy to 10.0.0.84
2. ⏸️ Verify all services accessible via IP:PORT
3. ⏸️ Configure DNS records
4. ⏸️ Set up Traefik for HTTPS/SSL
5. ⏸️ Run Playwright E2E tests
6. ⏸️ Set up monitoring (Prometheus + Grafana)
7. ⏸️ Configure backups

---

## 🔗 Quick Reference

**Current Access (Direct IP)**:
- Wizardsofts.com: http://10.0.0.84:3000
- Daily Deen Guide: http://10.0.0.84:3002
- Quant-Flow: http://10.0.0.84:3001

**Future Access (With DNS + Traefik)**:
- Wizardsofts.com: https://www.wizardsofts.com
- Daily Deen Guide: https://dailydeenguide.wizardsofts.com
- Quant-Flow: https://quant.wizardsofts.com
