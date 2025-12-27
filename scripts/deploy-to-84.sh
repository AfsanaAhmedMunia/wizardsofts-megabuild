#!/bin/bash
# Quick Deployment Script to 10.0.0.84
# Usage: ./scripts/deploy-to-84.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
DEPLOY_HOST="10.0.0.84"
DEPLOY_USER="deploy"
DEPLOY_PATH="/opt/wizardsofts-megabuild"
COMPOSE_PROFILE="all"  # Deploy everything: shared, gibd-quant, and web-apps

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deploying to 10.0.0.84${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if SSH key exists
if [ ! -f ~/.ssh/id_rsa ]; then
    echo -e "${RED}Error: SSH key not found at ~/.ssh/id_rsa${NC}"
    echo "Generate one with: ssh-keygen -t rsa -b 4096"
    exit 1
fi

# Test SSH connection
echo -e "${YELLOW}Testing SSH connection...${NC}"
if ssh -o ConnectTimeout=5 $DEPLOY_USER@$DEPLOY_HOST "echo 'Connection successful'" 2>/dev/null; then
    echo -e "${GREEN}✓ SSH connection successful${NC}"
else
    echo -e "${RED}✗ SSH connection failed${NC}"
    echo "Please ensure:"
    echo "  1. SSH key is added to $DEPLOY_HOST authorized_keys"
    echo "  2. Server is accessible from your network"
    exit 1
fi

# Sync files to server
echo -e "${YELLOW}Syncing files to server...${NC}"
rsync -avz --delete \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude 'target' \
    --exclude '.m2' \
    --exclude '.cache' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.env' \
    --progress \
    ./ $DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH/

echo -e "${GREEN}✓ Files synced${NC}"

# Execute deployment on server
echo -e "${YELLOW}Deploying services on server...${NC}"

ssh $DEPLOY_USER@$DEPLOY_HOST << ENDSSH
set -e

SUDO_PASSWORD="29Dec2#24"
cd $DEPLOY_PATH

echo "Pulling latest changes..."
git pull origin main || echo "Not a git repository, using rsync files"

echo "Creating .env if not exists..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "WARNING: Created .env from .env.example - UPDATE WITH ACTUAL VALUES!"
fi

echo "Stopping existing services..."
echo "\$SUDO_PASSWORD" | sudo -S docker compose --profile $COMPOSE_PROFILE down || true

echo "Building Docker images..."
echo "\$SUDO_PASSWORD" | sudo -S docker compose --profile $COMPOSE_PROFILE build

echo "Starting services..."
echo "\$SUDO_PASSWORD" | sudo -S docker compose --profile $COMPOSE_PROFILE up -d

echo "Waiting for services to start..."
sleep 15

echo "Checking service status..."
docker compose ps

echo "Deployment complete!"
ENDSSH

# Run health checks
echo ""
echo -e "${YELLOW}Running health checks...${NC}"
sleep 15

# Check Eureka
if curl -f -s http://$DEPLOY_HOST:8762/actuator/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Eureka (8762): UP${NC}"
else
    echo -e "${RED}✗ Eureka (8762): DOWN${NC}"
fi

# Check Gateway
if curl -f -s http://$DEPLOY_HOST:8080/actuator/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Gateway (8080): UP${NC}"
else
    echo -e "${RED}✗ Gateway (8080): DOWN${NC}"
fi

# Check Signal Service
if curl -f -s http://$DEPLOY_HOST:5001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Signal Service (5001): UP${NC}"
else
    echo -e "${RED}✗ Signal Service (5001): DOWN${NC}"
fi

# Check NLQ Service
if curl -f -s http://$DEPLOY_HOST:5002/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ NLQ Service (5002): UP${NC}"
else
    echo -e "${RED}✗ NLQ Service (5002): DOWN${NC}"
fi

# Check Calibration Service
if curl -f -s http://$DEPLOY_HOST:5003/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Calibration Service (5003): UP${NC}"
else
    echo -e "${RED}✗ Calibration Service (5003): DOWN${NC}"
fi

# Check Agent Service
if curl -f -s http://$DEPLOY_HOST:5004/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Agent Service (5004): UP${NC}"
else
    echo -e "${RED}✗ Agent Service (5004): DOWN${NC}"
fi

# Check Quant-Flow Frontend
if curl -f -s http://$DEPLOY_HOST:3001 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Quant-Flow Frontend (3001): UP${NC}"
else
    echo -e "${RED}✗ Quant-Flow Frontend (3001): DOWN${NC}"
fi

# Check Wizardsofts Corporate Website
if curl -f -s http://$DEPLOY_HOST:3000 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Wizardsofts.com (3000): UP${NC}"
else
    echo -e "${RED}✗ Wizardsofts.com (3000): DOWN${NC}"
fi

# Check Daily Deen Guide
if curl -f -s http://$DEPLOY_HOST:3002 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Daily Deen Guide (3002): UP${NC}"
else
    echo -e "${RED}✗ Daily Deen Guide (3002): DOWN${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Access your applications at:"
echo ""
echo "Web Applications:"
echo "  - Wizardsofts.com: http://$DEPLOY_HOST:3000"
echo "  - Daily Deen Guide: http://$DEPLOY_HOST:3002"
echo "  - Quant-Flow: http://$DEPLOY_HOST:3001"
echo ""
echo "Infrastructure Services:"
echo "  - Eureka Dashboard: http://$DEPLOY_HOST:8762"
echo "  - API Gateway: http://$DEPLOY_HOST:8080"
echo "  - Signal Service: http://$DEPLOY_HOST:5001"
echo "  - NLQ Service: http://$DEPLOY_HOST:5002"
echo "  - Calibration Service: http://$DEPLOY_HOST:5003"
echo "  - Agent Service: http://$DEPLOY_HOST:5004"
echo ""
echo "To view logs:"
echo "  ssh $DEPLOY_USER@$DEPLOY_HOST 'cd $DEPLOY_PATH && docker compose logs -f'"
echo ""
