#!/bin/bash

until nc -z ${RABBITMQ_HOST} ${RABBITMQ_PORT}; do
    echo "$(date) - waiting for rabbitmq..."
    sleep 2
done

# alembic upgrade head

nameko run --config config.yaml src.db_service --backdoor 3000