#!/bin/bash

until nc -z ${RABBITMQ_HOST} ${RABBITMQ_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 2
done

until nc -z ${REDIS_HOST} ${REDIS_PORT}; do
    echo "$(date) - waiting for redis..."
    sleep 2
done

nameko run --config /app/config.yaml src.cache_service --backdoor 3000
