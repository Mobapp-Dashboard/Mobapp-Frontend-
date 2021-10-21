#! /usr/bin/env sh

# Exit in case of error
set -e

VERSION=1.0.0 \
TARGET=LIVE \
DOMAIN=dash.klh.criptofesta.org \
STACK_NAME=mobdash \
docker-compose \
-f docker-compose.yml \
config > docker-stack.yml

docker-auto-labels docker-stack.yml

docker stack rm "${STACK_NAME}"
docker stack deploy -c docker-stack.yml --with-registry-auth "${STACK_NAME?Variable not set}"
