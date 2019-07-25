#!/usr/bin/env bash

# (Re-)Start the MIP
# check logs with:
# docker-compose logs -f

set -xe

# Build containers to include updates
# "#################################################################################################################"
echo "Build MIP Components"
# "#################################################################################################################"
docker-compose build
docker-compose pull

# Stop Platform, if it is already running
docker-compose down || True

# Deploy MIP
# "#################################################################################################################"
echo "Deploy MIP"
# "#################################################################################################################"
docker-compose up

# Show logs
# "#################################################################################################################"
echo "Deployment finished showing logs (terminate log monitor with CTRL + C)"
# "#################################################################################################################"
#docker-compose logs -f
