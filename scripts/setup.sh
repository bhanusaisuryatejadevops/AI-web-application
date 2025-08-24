#!/usr/bin/env bash
set -euo pipefail

NAMESPACE=devops-ai

kubectl apply -f kubernetes/namespace.yaml

# Secrets
kubectl -n $NAMESPACE create secret generic ai-secrets --from-literal=hf_api_token="${HUGGINGFACE_API_TOKEN:-CHANGEME}" --dry-run=client -o yaml | kubectl apply -f -
kubectl -n $NAMESPACE create secret generic grafana-secrets --from-literal=admin_password="${GRAFANA_ADMIN_PASSWORD:-admin123}" --dry-run=client -o yaml | kubectl apply -f -

# Deploy app
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml

# Monitoring
kubectl apply -f kubernetes/monitoring/prometheus.yaml
kubectl apply -f kubernetes/monitoring/grafana.yaml

echo "Deployed. Port-forward with:"
echo "kubectl -n $NAMESPACE port-forward svc/ai-app-svc 8080:80"
echo "kubectl -n $NAMESPACE port-forward svc/prometheus-svc 9090:9090"
echo "kubectl -n $NAMESPACE port-forward svc/grafana-svc 3000:3000"
