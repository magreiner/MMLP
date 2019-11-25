#!/usr/bin/env bash

# (Re-)Start the MMLP
# check logs with:
# docker-compose logs -f

set -xe

# Build containers to include updates
# "#################################################################################################################"
echo "Build MMLP Components"
# "#################################################################################################################"
docker-compose build
docker-compose pull

# Stop Platform, if it is already running
docker-compose down || True

# Deploy MMLP
# "#################################################################################################################"
echo "Deploy MMLP"
# "#################################################################################################################"
docker-compose up

# Show logs
# "#################################################################################################################"
echo "Deployment finished showing logs (terminate log monitor with CTRL + C)"
# "#################################################################################################################"
#docker-compose logs -f
