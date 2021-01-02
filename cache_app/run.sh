#!/bin/bash

until nc -z ${RABBIT_HOST} ${RABBIT_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 2
done

nameko run --config /app/config.yaml src.cache_service --backdoor 3000
