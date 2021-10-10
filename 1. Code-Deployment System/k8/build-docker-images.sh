echo "Building docker images"

echo "Building repo-listener image"
docker build -t repo-listener ../repo-listener-app/

echo "Building worker-monitor image"
docker build -t worker-monitoring-app ../worker-monitoring-app/

echo "Building worker-app image"
docker build -t worker-app ../worker-app/

echo "Building client-app image"
docker build -t client-app ../client-app/

echo "Docker images build complete"