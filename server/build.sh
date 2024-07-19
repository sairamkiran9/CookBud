# Build the latest docker image from the latest backend 
docker build -t recsys:latest .
# Start the container and expose it on port 8000
docker run -p 8000:8000 -d recsys:latest