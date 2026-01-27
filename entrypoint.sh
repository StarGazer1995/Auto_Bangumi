#!/bin/bash
# shellcheck shell=bash

umask ${UMASK}

if [ -f /config/bangumi.json ]; then
    mv /config/bangumi.json /app/data/bangumi.json
fi

groupmod -o -g "${PGID}" ab
usermod -o -u "${PUID}" ab

chown ab:ab -R /app /home/ab

if [ $# -eq 0 ]; then
    set -- /app/.venv/bin/python main.py
fi

exec su-exec "${PUID}:${PGID}" "$@"