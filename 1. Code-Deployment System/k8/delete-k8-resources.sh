#!/bin/bash

echo "Deleting configmaps"
kubectl delete -f config-maps/
echo "Configmaps deleted"

echo "Delete all deployments"
kubectl delete all --all
echo "All deployments deleted"