from django.core.management.base import BaseCommand
from django.conf import settings

import sys
import signal
import ast
import importlib
from redis import Redis


def stop(signum, frame):
    sys.exit()


signal.signal(signal.SIGINT, stop)


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.__check_config()
        redis = Redis(**settings.REDIS_PUBSUB)
        sub = redis.pubsub()
        sub.subscribe(settings.CHANNELS_SUB)
        for msg in sub.listen():
            print(f'message: {msg}')
            if msg.get('type') == 'message':
                data = ast.literal_eval(msg.get('data').decode())
                self.run_tasks(data=data)

    @staticmethod
    def run_tasks(data):
        for task in settings.TASKS_SUB:
            task_name = task.get('task_name')
            task_string = task.get('task')
            if task_name == data.get('task_name'):
                module_string, func = '.'.join(task_string.split('.')[:-1]), task_string.split('.')[-1]
                try:
                    module = importlib.import_module(module_string)
                except ImportError:
                    return f'Module `{task_string}` not found'
                if not hasattr(module, func):
                    return f'Task `{func}` in `{module_string}` not found.'
                async_task = getattr(module, func)
                print(f'running task: {task_name}')
                async_task.delay(data=data)

    @staticmethod
    def __check_config():
        assert settings.CHANNELS_SUB, 'Must be set `CHANNELS_SUB` in settings.'
        assert settings.TASKS_SUB, 'Must be set `TASKS_SUB` in settings.'

