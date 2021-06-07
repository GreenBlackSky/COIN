"""Create and configurate celery."""

import os

from celery import Celery

celery_app = Celery(
    'core_app',
    broker='amqp://{}:{}@{}:{}//'.format(
        os.environ['RABBITMQ_DEFAULT_USER'],
        os.environ['RABBITMQ_DEFAULT_PASS'],
        os.environ['RABBITMQ_HOST'],
        os.environ['RABBITMQ_PORT']
    ),
    backend='rpc://'
)
