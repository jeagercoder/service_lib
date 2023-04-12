from rest_framework.response import Response
from rest_framework import status

import requests
from urllib.parse import urljoin


class InternalService:

    def __init__(self, **kwargs):
        self.service_name = None
        self.context = kwargs.get('context')

    def get_host(self):
        raise NotImplementedError('`get_host()` must be implemented.')

    def get_headers(self):
        raise NotImplementedError('`get_headers()` must be implemented.')

    def get_url(self):
        return urljoin(self.get_host(), self.context.get('view').get_route())

    def get_kwargs_request(self):
        request = self.context.get('request')
        return {
            'data': request.data,
            'json': request.data,
            'files': request.FILES,
            'params': request.query_params,
            'headers': self.get_headers()
        }

    def __request(self, method: str, url: str, **kwargs):
        try:
            response = requests.request(
                method=method,
                url=self.get_url(),
                **kwargs
            )
            return Response(data=response.json(), status=response.status_code)
        except requests.exceptions.HTTPError:
            return Response({'detail': f'Service {self.service_name} not available.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def post_json(self):
        kwargs = self.get_kwargs_request()
        kwargs.pop('data')
        kwargs.pop('files')
        return self.__request(method='post', url=self.get_url(), **kwargs)

    def get_json(self):
        kwargs = self.get_kwargs_request()
        return self.__request(method='get', url=self.get_url(), **kwargs)

