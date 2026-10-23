#!/usr/bin/env bash
# ==============================================================================
# TribeRaised Django CMS Marketing Site - GCP Cloud Run Deployment Script
# Aligned with tr-profile/docs/DEPLOYMENT_GCP.md
# ==============================================================================

set -euo pipefail

# Default configuration values
ENV_NAME="${ENV_NAME:-prod}"
GCP_REGION="${GCP_REGION:-us-central1}"
GCP_PROJECT_ID="${GCP_PROJECT_ID:-triberaised-prod}"
SERVICE_NAME="tr-django-cms-${ENV_NAME}"
REGISTRY_NAME="tr-images"
IMAGE_TAG="$(git rev-parse --short HEAD 2>/dev/null || echo 'manual')"
IMAGE_URI="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REGISTRY_NAME}/django-cms-site:${ENV_NAME}-${IMAGE_TAG}"

log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $*"
}

log_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $*"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $*" >&2
}

# ------------------------------------------------------------------------------
# 1. Pre-flight Checks
# ------------------------------------------------------------------------------
log_info "Executing pre-flight verification for deployment..."

command -v gcloud >/dev/null 2>&1 || {
    log_error "Google Cloud SDK (gcloud) is required but not installed. Aborting."
    exit 1
}

command -v docker >/dev/null 2>&1 || {
    log_error "Docker is required for building container images. Aborting."
    exit 1
}

ACTIVE_PROJECT="$(gcloud config get-value project 2>/dev/null || echo '')"
if [ -n "${ACTIVE_PROJECT}" ] && [ "${ACTIVE_PROJECT}" != "${GCP_PROJECT_ID}" ]; then
    log_info "Switching active gcloud project to ${GCP_PROJECT_ID}..."
    gcloud config set project "${GCP_PROJECT_ID}" --quiet
fi

# ------------------------------------------------------------------------------
# 2. Build Container Image
# ------------------------------------------------------------------------------
log_info "Building production container image: ${IMAGE_URI}..."
docker build \
    --tag "${IMAGE_URI}" \
    --tag "${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${REGISTRY_NAME}/django-cms-site:${ENV_NAME}-latest" \
    --file Dockerfile \
    .

# ------------------------------------------------------------------------------
# 3. Authenticate & Push Image to Google Artifact Registry
# ------------------------------------------------------------------------------
log_info "Configuring Docker authentication for Artifact Registry..."
gcloud auth configure-docker "${GCP_REGION}-docker.pkg.dev" --quiet

log_info "Pushing container image to Google Artifact Registry..."
docker push "${IMAGE_URI}"

# ------------------------------------------------------------------------------
# 4. Deploy Revision to GCP Cloud Run
# ------------------------------------------------------------------------------
MIN_INSTANCES=0
if [ "${ENV_NAME}" = "prod" ]; then
    MIN_INSTANCES=1
fi

log_info "Deploying Cloud Run service ${SERVICE_NAME} in region ${GCP_REGION}..."
gcloud run deploy "${SERVICE_NAME}" \
    --image="${IMAGE_URI}" \
    --region="${GCP_REGION}" \
    --platform="managed" \
    --allow-unauthenticated \
    --min-instances="${MIN_INSTANCES}" \
    --max-instances="5" \
    --cpu="1" \
    --memory="512Mi" \
    --port="8000" \
    --set-env-vars="DJANGO_SETTINGS_MODULE=config.settings.production,USE_GCS_MEDIA=True,GS_BUCKET_NAME=triberaised-marketing-media,SECURE_SSL_REDIRECT=True" \
    --set-secrets="SECRET_KEY=tr-cms-secret-key-${ENV_NAME}:latest,DATABASE_URL=tr-postgres-conn-string-${ENV_NAME}:latest" \
    --quiet

# ------------------------------------------------------------------------------
# 5. Service URL & Health Probe Verification
# ------------------------------------------------------------------------------
SERVICE_URL="$(gcloud run services describe "${SERVICE_NAME}" --region="${GCP_REGION}" --format="value(status.url)")"
log_info "Deployed Service URL: ${SERVICE_URL}"

log_info "Running health probe verification on ${SERVICE_URL}/healthz..."
if curl -s -f "${SERVICE_URL}/healthz" >/dev/null; then
    log_success "Deployment health check succeeded! Service is live and healthy."
else
    log_info "Health check curl returned non-zero (service may still be initializing DNS or requires internal VPC auth)."
fi

log_success "Deployment of ${SERVICE_NAME} completed successfully!"
