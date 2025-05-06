#!/bin/bash

# Exit on error
set -e

# Default environment is dev
ENV=${1:-dev}
NAMESPACE="recruitment-agent"

echo "Deploying recruitment agent to $ENV environment..."

# Build the Docker image
echo "Building Docker image..."
docker build -t recruitment-agent:latest .

# Check if namespace exists, create if it doesn't
kubectl get namespace $NAMESPACE > /dev/null 2>&1 || kubectl create namespace $NAMESPACE

# Apply Kustomize configuration
echo "Applying Kubernetes manifests for $ENV environment..."
kubectl apply -k infra/k8s/overlays/$ENV -n $NAMESPACE

# Wait for deployment to complete
echo "Waiting for deployment to complete..."
kubectl rollout status deployment/recruitment-agent -n $NAMESPACE

echo "Deployment completed successfully!"
echo "You can access the application with: kubectl port-forward svc/recruitment-agent 8000:80 -n $NAMESPACE"
