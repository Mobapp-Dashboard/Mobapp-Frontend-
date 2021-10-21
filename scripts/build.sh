#! /usr/bin/env sh

# Exit in case of error
set -e


VERSION=1.0.0 \
TARGET=LIVE \
DOMAIN=dash.klh.criptofesta.org \
STACK_NAME=mobdash \
docker-compose \
-f docker-compose.yml \
build
