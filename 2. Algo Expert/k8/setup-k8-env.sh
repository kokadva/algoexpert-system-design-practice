#!/bin/bash
echo "Welcome, Starting K8 Setup"

echo "Setting up ingress-nginx controller"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml
