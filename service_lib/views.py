from rest_framework.viewsets import GenericViewSet


class ServiceViewSet(GenericViewSet):
    route = None
    service_class = None

    def get_route(self):
        if not self.route:
            raise ValueError('route attribute must be set.')
        return self.route

    def get_service(self, **kwargs):
        service_class = self.get_service_class()
        kwargs.setdefault('context', self.get_service_context())
        return service_class(**kwargs)

    def get_service_class(self, **kwargs):
        if not self.service_class:
            raise ValueError('service_class attribute must be set.')
        return self.service_class

    def get_service_context(self):
        return {
            'request': self.request,
            'view': self
        }


