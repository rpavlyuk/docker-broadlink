#!/bin/bash

set -e

VERSION="1.0"
CONTAINER_NAME="docker.io/rpavlyuk/c7-broadlink"

# Run svarog to build the RPMs
svarog || { 
  echo "WARNING: SVAROG exit code $?"
}

# collect packages
rm -rf .rpms && mkdir -p .rpms || exit 1
find ./.repo -type f -name "*.rpm" -exec cp {} ./.rpms \; || exit 1

# Build docker container
docker build --rm -t "$CONTAINER_NAME" .
