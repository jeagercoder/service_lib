from django.core.cache import cache
from django.conf import settings

import random
import string


def login(uuid, username, email):
    session = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for n in range(64))
    if len(cache.keys(f'{session}_*')) != 0:
        return login(uuid, username, email)
    session = f'{session}_{uuid}'
    cache.set(session, {'uuid': uuid,
                        'username': username,
                        'email': email}, settings.SESSION_EXPIRED)
    return session.split('_')[0]
