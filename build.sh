#!/bin/bash

VERSION="1.0"
CONTAINER_NAME="docker.io/rpavlyuk/c7-ls30"

# Run svarog to build the RPMs
svarog

# collect packages
rm -rf .rpms && mkdir -p .rpms
find ./.repo -type f -name "*.rpm" -exec cp {} ./.rpms \;

# Build docker container
docker build --rm -t $CONTAINER_NAME .
