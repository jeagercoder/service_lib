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

### Middleware
```python
# settings.py
MIDDLEWARE = [
    'service_lib.middleware.InternalServiceMiddleware',
    ...
]
```

### Service communication (for api gateway)
```python
from django.conf import settings

from rest_framework.decorators import action

from service_lib.services import InternalService
from service_lib.views import ServiceViewSet


class AuthService(InternalService):

    def get_host(self):
        return settings.AUTH_SERVICE_URL

    def get_headers(self):
        return {'Authorization': settings.AUTH_SERVICE_AUTH}

class AccountViewSet(ServiceViewSet):
    service_class = AuthService
    route = '/path/login'

    @action(methods=['POST'], detail=False)
    def register(self, request):
        service = self.get_service()
        return service.post_json()
```