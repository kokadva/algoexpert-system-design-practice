#!/bin/bash
echo "Welcome, Starting K8 Setup"

echo "Setting up Config Maps"
kubectl apply -f config-maps/
echo "Config Maps setup complete!"

echo "Setting up Gitea Repository, Minio Object Storage, Postgresql DB"
kubectl apply -f gitea-repository-deployment.yaml
kubectl apply -f minio-object-storage-deployment.yaml
kubectl apply -f queue-db-deployment.yaml
echo "Gitea Repository, Minio Object Storage, Postgresql DB setup complete!"

sleep 5s

echo "Setting up repo-listener, worker-monitor, worker, client apps"
kubectl apply -f repository-listener-deployment.yaml
kubectl apply -f worker-monitor-deployment.yaml
kubectl apply -f worker-app-deployment.yaml
kubectl apply -f client-app-deployment.yaml
echo "repo-listener, worker-monitor, worker, client apps setup complete!"

echo "K8 Setup compelte"
