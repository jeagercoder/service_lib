from django.conf import settings

import requests
from urllib.parse import urljoin


class Helper:

    def __init__(self, route):
        self.route = route
        self.response_json = None
        self.status_code = None

    def get_headers(self):
        raise NotImplementedError('`get_headers()` must be implemented.')

    def get_url(self):
        raise NotImplementedError('`get_url()`, must be implemented.')

    def __request_with_json_response(self, method, url, **kwargs):
        response = requests.request(method=method, url=url, **kwargs)
        self.response_json = response.json()
        self.status_code = response.status_code

    def post_json(self, json=None, params=None):
        kwargs = {'json': json, 'params': params, 'headers': self.get_headers()}
        return self.__request_with_json_response(method='post', url=self.get_url(), **kwargs)


class NotificationHelper(Helper):

    def get_headers(self):
        return {'Proxy-Authorization': settings.NOTIFICATION_SERVICE_AUTH}

    def get_url(self):
        return urljoin(settings.NOTIFICATION_SERVICE_URL, self.route)
