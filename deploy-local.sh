#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# TribeRaised Django CMS Marketing Site — Local Docker Orchestration Script
# ==============================================================================
# Deploys:
#   - Django CMS Marketing Site (Port 8001 -> Container 8000)
#   - Connects to shared triberaised_tr-network & tr-profile-postgres
#
# Flags:
#   --standalone    Runs with local isolated postgres container (no dependency
#                   on triberaised monorepo stack)
#   --build         Forces rebuild of container image
# ==============================================================================

BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

STANDALONE=false
FORCE_BUILD=false

for arg in "$@"; do
    case "$arg" in
        --standalone)
            STANDALONE=true
            ;;
        --build)
            FORCE_BUILD=true
            ;;
        *)
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Source environment variables if .env exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
elif [ -f .env.example ]; then
    echo -e "${YELLOW}Notice: .env not found. Copying defaults from .env.example...${NC}"
    cp .env.example .env
    set -a
    source .env
    set +a
fi

PORT="${PORT:-8001}"
POSTGRES_DB="${POSTGRES_DB:-triberaised_cms}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"

echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}  TribeRaised Marketing CMS — Local Docker Deployment Pipeline ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}\n"

# 1. Check Docker Daemon
echo -e "${BLUE}[1/5] Checking Docker daemon status...${NC}"
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker daemon is not running. Please start Docker and retry.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker daemon is active.${NC}\n"

# 2. Check / Setup Network
COMPOSE_FILE="docker-compose.local.yml"
if [ "$STANDALONE" = true ]; then
    COMPOSE_FILE="docker-compose.standalone.yml"
    echo -e "${BLUE}[2/5] Operating in STANDALONE mode with dedicated database...${NC}"
    echo -e "${CYAN}Using compose file: ${COMPOSE_FILE}${NC}\n"
else
    echo -e "${BLUE}[2/5] Checking shared Docker network (triberaised_tr-network)...${NC}"
    if ! docker network inspect triberaised_tr-network > /dev/null 2>&1; then
        echo -e "${YELLOW}Network 'triberaised_tr-network' not found. Creating it now...${NC}"
        docker network create triberaised_tr-network
        echo -e "${GREEN}✓ Created bridge network 'triberaised_tr-network'.${NC}\n"
    else
        echo -e "${GREEN}✓ Network 'triberaised_tr-network' is active.${NC}\n"
    fi
fi

# 3. Build Docker Image
echo -e "${BLUE}[3/5] Building Django CMS container image (tr-django-cms)...${NC}"
BUILD_ARGS=""
if [ "$FORCE_BUILD" = true ]; then
    BUILD_ARGS="--no-cache"
fi
docker compose -f "$COMPOSE_FILE" build $BUILD_ARGS
echo -e "${GREEN}✓ Container image built successfully.${NC}\n"

# 4. Spin Up Services in Detached Mode
echo -e "${BLUE}[4/5] Launching container services in detached mode...${NC}"
docker compose -f "$COMPOSE_FILE" up -d
echo -e "${GREEN}✓ Container launched.${NC}\n"

# 5. Summary & Useful Commands
echo -e "${BLUE}[5/5] Docker Container Status:${NC}"
docker compose -f "$COMPOSE_FILE" ps

echo -e "\n${BOLD}${GREEN}================================================================${NC}"
echo -e "${BOLD}${GREEN}  Deployment Initialization Completed!                         ${NC}"
echo -e "${BOLD}${GREEN}================================================================${NC}"
echo -e "  ${BOLD}Marketing Site:${NC}      http://localhost:${PORT}/"
echo -e "  ${BOLD}Admin Dashboard:${NC}     http://localhost:${PORT}/admin/"
echo -e "  ${BOLD}Health Probe:${NC}        http://localhost:${PORT}/healthz"
echo -e "\n  Useful Commands:"
echo -e "    View Logs:         ${YELLOW}docker compose -f ${COMPOSE_FILE} logs -f web${NC}"
echo -e "    Create Superuser:  ${YELLOW}docker compose -f ${COMPOSE_FILE} exec web python manage.py createsuperuser${NC}"
echo -e "    Run Migrations:    ${YELLOW}docker compose -f ${COMPOSE_FILE} exec web python manage.py migrate${NC}"
echo -e "    Stop Stack:        ${YELLOW}docker compose -f ${COMPOSE_FILE} down${NC}"
echo -e "${BOLD}${GREEN}================================================================${NC}\n"
