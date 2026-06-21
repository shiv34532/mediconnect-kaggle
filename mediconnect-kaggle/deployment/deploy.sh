#!/bin/bash
# MediConnect Deployment Script
# Demonstrates: Deployability (one-click deployment)
# Usage: bash deployment/deploy.sh

set -e  # Exit on error

echo "=========================================="
echo "  MediConnect Deployment to Cloud Run"
echo "=========================================="

# Configuration
PROJECT_ID=${PROJECT_ID:-your-gcp-project}
REGION=${REGION:-us-central1}
SERVICE_NAME=${SERVICE_NAME:-mediconnect}
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo ""
echo "Step 1: Building Docker image..."
docker build -t ${IMAGE_NAME}:latest -f deployment/Dockerfile .

echo ""
echo "Step 2: Pushing to Google Container Registry..."
docker push ${IMAGE_NAME}:latest

echo ""
echo "Step 3: Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME}   --image ${IMAGE_NAME}:latest   --region ${REGION}   --platform managed   --allow-unauthenticated   --port 8000   --memory 1Gi   --cpu 1   --max-instances 10   --min-instances 1   --set-secrets GOOGLE_API_KEY=google-api-key:latest   --set-secrets ENCRYPTION_KEY=encryption-key:latest

echo ""
echo "=========================================="
echo "  Deployment Complete!"
echo "=========================================="
echo "Service URL: $(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)')"
echo ""
echo "To test: curl $(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)')/health"
echo ""
