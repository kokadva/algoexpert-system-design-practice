#!/bin/bash
echo "Welcome, Starting K8 Setup"

kubectl apply -f config-maps/questions-db-configmap.yaml

echo "Setting up ingress-nginx controller"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f ingress.yaml

kubectl apply -f questions-db-deployment.yaml

sleep 5s

kubectl apply -f question-solution-checker-app-deployment.yaml
kubectl apply -f questions-server-app-deployment.yaml
kubectl apply -f solution-tester-worker-app-deployment.yaml
kubectl apply -f static-web-app-deployment.yaml
