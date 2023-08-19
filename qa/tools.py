from datetime import datetime, timedelta
import random
import string
from django.contrib.auth.models import User
from qa.models import Session


def key_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def do_login(username, password):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None

    if not user.check_password(password):
        return None

    session = Session()
    session.key = key_generator()
    session.user = user
    session.expires = datetime.now() + timedelta(days=3)
    session.save()
    return session
