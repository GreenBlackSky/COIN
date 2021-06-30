"""Create and configurate celery."""

import os
from functools import partial

from celery import Celery

from common.debug_tools import log_function, log_method


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
    Implemetation class, that inherits from interface, must implement every
    interface method.
    Due to stateless oriented design, use only static methods.
    """
    def __new__(cls, name, bases, dct):
        """Create new type with remove service calls."""
        if not bases:
            # first generation is interface, replace it's methods with caslls
            for attr_name in dct:
                if not attr_name.startswith('__'):
                    dct[attr_name] = partial(
                        log_function(_call_celery_task),
                        '.'.join((name, attr_name))
                    )
        elif len(bases) == 1:
            # second generation is implementation,
            # check if all public methods are implemented
            # and register them as tasks
            (base,) = bases
            base_methods = {
                method_name for method_name in dir(base)
                if not method_name.startswith('_')
            }
            child_methods = {
                method_name for method_name in dct
                if not (method_name.startswith('_'))
            }
            if base_methods != child_methods:
                raise Exception("Implementation does not fit interface")
            for method_name in child_methods:
                method = log_function(dct[method_name])
                task_name = '.'.join((base.__name__, method_name))
                dct[method_name] = celery_app.task(name=task_name)(method)
        else:
            raise Exception("Third generation! Honestly, idk what to do")
        return super().__new__(cls, name, bases, dct)
