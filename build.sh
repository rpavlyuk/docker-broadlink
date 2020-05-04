#!/bin/bash

VERSION="1.0"
CONTAINER_NAME="docker.io/rpavlyuk/c7-broadlink"

# Run svarog to build the RPMs
svarog || exit 1

# collect packages
rm -rf .rpms && mkdir -p .rpms || exit 1
find ./.repo -type f -name "*.rpm" -exec cp {} ./.rpms \; || exit 1

# Build docker container
docker build --rm -t $CONTAINER_NAME .
