# service_lib

### Pubsub
```python
# settings.py
INSTALLED_APPS = [
    ...,
    'service_lib.pubsub'
]

REDIS_PUBSUB = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 4,
    'password': 'pass'
}

CHANNELS_SUB = (
    'notification'
)

TASKS_SUB = [
    {
        'task_name': 'otp_register',
        'task': 'notification.tasks.send_otp_register'
    }
]
```