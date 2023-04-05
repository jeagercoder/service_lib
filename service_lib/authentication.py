from django.core.cache import cache
from django.contrib.auth import get_user_model

from rest_framework.authentication import BaseAuthentication


class SessionAuthentication(BaseAuthentication):

    def authenticate(self, request):
        session = request.COOKIES.get('session')
        if session is None:
            return None
        sessions = cache.keys(f'{session}_*')
        if len(sessions) != 1:
            return None
        session = sessions[0]

        data = cache.get(session)
        if data is None:
            return None

        account = get_user_model()
        account.uuid = data.get('uuid')
        account.username = data.get('username')
        account.email = data.get('email')

        return account, session
