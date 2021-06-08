"""Create and configurate celery."""

import os
from functools import partial, wraps

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


def _call_celery_task(task_name, **kargs):
    return celery_app.send_task(task_name, kwargs=kargs).get()


class CeleryProxyMetaClass(type):
    """
    Magic metaclass.

    Transforms api mock methods into remote service calls.
    In order to use it, class must have service_path attribute.
    Also, args must be passed explicitly.
    """

    def __new__(cls, name, bases, dct):
        """Create new type with remove service calls."""
        service_path = dct['service_path']
        for attr_name in dct:
            if (
                not attr_name.startswith('__') and
                not attr_name == "service_path"
            ):

                dct[attr_name] = partial(
                    _call_celery_task,
                    '.'.join((service_path, attr_name))
                )
        return super().__new__(cls, name, bases, dct)
