#!/bin/bash

until nc -z ${RABBITMQ_HOST} ${RABBITMQ_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 2
done

until nc -z ${POSTGRES_HOST} ${POSTGRES_PORT}; do
    echo "$(date) - waiting for postgres..."
    sleep 2
done

nameko run --config config.yaml src.db_service --backdoor 3000