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

    # TODO check signature
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


#  trying to make it less messy, maybe instantiate this classes somehow....
class _CeleryProxyMetaBase(type):
    def __new__(cls, name, bases, dct):
        if not bases:
            # our base class, he's ok, don't bother him
            return super(_CeleryProxyMetaBase, cls).__new__(
                cls, name, bases, dct
            )
        elif len(bases) == 1:
            # first generation is interface, replace it's methods with caslls
            for attr_name in dct:
                if not attr_name.startswith('__'):

                    @log_method
                    def _wrapper(self, *args, **kargs):
                        return bases[0].__call_celery_task(
                            self, '.'.join((name, attr_name)), *args, **kargs
                        )

                    dct[attr_name] = _wrapper
        elif len(bases) == 2:
            # second generation is implementation,
            # check if all public methods are implemented
            # and register them as tasks

            _, interface = bases
            base_methods = {
                method_name for method_name in dir(interface)
                if not method_name.startswith('_')
            }
            child_methods = {
                method_name for method_name in dct
                if not (method_name.startswith('_'))
            }
            if base_methods != child_methods:
                raise Exception("Implementation does not fit interface")
            # for method_name in child_methods:
            #     task_name = '.'.join((interface.__name__, method_name))
            #     method = log_function(dct[method_name])
            #     dct[method_name] = celery_app.task(name=task_name)(method)
        else:
            raise Exception("Third generation! Honestly, idk what to do")
        return super().__new__(cls, name, bases, dct)


class CeleryProxyBase(metaclass=_CeleryProxyMetaBase):

    class _Stub:
        pass

    __focus = _Stub()

    def __init__(self, rabbit_user, rabbit_pass, rabbit_host, rabbit_port):
        self._celery_app = Celery(
            'core_app',
            broker='amqp://{}:{}@{}:{}//'.format(
                rabbit_user,
                rabbit_pass,
                rabbit_host,
                rabbit_port
            ),
            backend='rpc://'
        )

    def __call_celery_task(self, task_name, **kargs):
        return self._celery_app.send_task(task_name, kwargs=kargs).get()
