#!/usr/bin/env bash

# (Re-)Start the MMLP
# check logs with:
# docker-compose logs -f

# Stop if error occurs
set -e

# Build containers to include updates
# "#################################################################################################################"
echo "Build MMLP Components"
# "#################################################################################################################"
# docker-compose pull
docker-compose build --pull

# Deploy MMLP
# "#################################################################################################################"
echo "Deploy MMLP"
# "#################################################################################################################"
# Perform a clean shutdown of the Platform, if it is already running
docker-compose down || true

# Start the Platform (old data from persistent volumes will be used - delete manually for clean start)
docker-compose up -d

# Show logs
# "#################################################################################################################"
# echo "Deployment finished showing logs (terminate log monitor with CTRL + C)"
# "#################################################################################################################"
# docker-compose logs -f
