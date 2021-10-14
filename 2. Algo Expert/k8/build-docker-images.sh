echo "Building docker images"

echo "Building question-solution-checker-app"
docker build -t question-solution-checker-app ../question-solution-checker-app/

echo "Building questions-server-app image"
docker build -t questions-server-app ../questions-server-app/

echo "Building solution-tester-worker-app image"
docker build -t solution-tester-worker-app ../solution-tester-worker-app/

echo "Building static-website-app image"
docker build -t static-website-app ../static-website-app/

echo "Pulling imges from dockerhub"
docker pull postgres:9.6

echo "Docker images build complete"