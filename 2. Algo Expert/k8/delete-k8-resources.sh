#!/bin/bash

echo "Deleting configmaps"
kubectl delete -f config-maps/
echo "Configmaps deleted"

echo "Delete ingress setup"
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.4/deploy/static/provider/cloud/deploy.yaml
kubectl delete -f ingress.yaml
echo "Ingress deleted"

echo "Delete all deployments"
kubectl delete all --all
echo "All deployments deleted"