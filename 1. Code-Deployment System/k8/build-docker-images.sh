echo "Building docker images"

echo "Building repo-listener image"
docker build -t repo-listener ../repo-listener-app/

echo "Building worker-monitor image"
docker build -t worker-monitoring-app ../worker-monitoring-app/

echo "Building worker-app image"
docker build -t worker-app ../worker-app/

echo "Building client-app image"
docker build -t client-app ../client-app/

echo "Pulling imges from dockerhub"
docker pull gitea/gitea:1.15.3
docker pull postgres:9.6
docker pull minio/minio


echo "Docker images build complete"