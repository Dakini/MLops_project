#!/usr/bin/env bash

if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

docker-compose up  --build -d

sleep 5
