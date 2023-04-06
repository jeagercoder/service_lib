from django.shortcuts import HttpResponse
from django.conf import settings

import json


class InternalServiceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        message = json.dumps({'detail': 'Authentication Internal Service Required.'})
        resp = HttpResponse(
                message,
                status=403,
                content_type='application/json'
            )
        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth is None:
            return resp
        auth = auth.split(' ')
        if len(auth) != 2:
            return resp
        if auth[0] != settings.INTERNAL_AUTH_PREFIX or auth[1] != settings.INTERNAL_AUTH_VALUE:
            return resp
        response = self.get_response(request)
        return response
