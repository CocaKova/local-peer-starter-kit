#!/bin/bash

# Local Peer Starter Kit Setup
# ----------------------------
# Version: 1.0
# Sets up Ollama + Open WebUI + Qdrant via Docker Compose.

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==> Initializing Local Peer Starter Kit v1.0 <==${NC}"

# 1. Hardware/Driver Check
echo -e "\n${BLUE}[1/4] Checking Hardware Environment...${NC}"
if ! command -v nvidia-smi &> /dev/null; then
    echo -e "${RED}Error: NVIDIA drivers not found. This kit requires an NVIDIA GPU.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ NVIDIA drivers detected.${NC}"

# 2. Docker Check
echo -e "\n${BLUE}[2/4] Checking Docker Installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed. Please install Docker Engine before proceeding.${NC}"
    exit 1
fi
if ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: Docker Compose V2 is required.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker and Compose detected.${NC}"

# 3. Environment Setup
echo -e "\n${BLUE}[3/4] Configuring Environment...${NC}"
if [ ! -f .env ]; then
    echo -e "Creating .env from .env.example..."
    cp .env.example .env
    # Generate a random secret key instead of shipping a guessable default.
    SECRET=$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n')
    if [ -n "$SECRET" ]; then
        sed -i "s|^WEBUI_SECRET_KEY=.*|WEBUI_SECRET_KEY=${SECRET}|" .env
        echo -e "${GREEN}✓ .env created with a freshly generated WEBUI_SECRET_KEY.${NC}"
    else
        echo -e "${GREEN}✓ .env created.${NC} ${RED}Could not auto-generate a secret — set WEBUI_SECRET_KEY manually before exposing this host.${NC}"
    fi
else
    echo -e "${GREEN}✓ .env already exists. Skipping.${NC}"
fi

# 4. Deployment
echo -e "\n${BLUE}[4/4] Deploying Local Peer Stack...${NC}"
docker compose pull
docker compose up -d

echo -e "\n${GREEN}================================================================${NC}"
echo -e "${GREEN}  🚀 LOCAL PEER STACK DEPLOYED SUCCESSFULLY${NC}"
echo -e "${GREEN}================================================================${NC}"
echo -e "Open WebUI: http://localhost:3000"
echo -e "Ollama API: http://localhost:11434"
echo -e "Qdrant Dashboard: http://localhost:6333/dashboard"
echo -e "\nNext Step: Open WebUI -> Settings -> Models -> Pull a model (e.g., 'llama3')"
echo -e "${GREEN}================================================================${NC}"
