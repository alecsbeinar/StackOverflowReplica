from datetime import datetime

from django.http import HttpRequest
from django.utils.timezone import make_aware

from qa.models import Session


class CheckSessionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            sessid = request.COOKIES.get('sessid')
            session = Session.objects.get(
                key=sessid,
                expires__gt=make_aware(datetime.now()),
            )
            request.session = session
            request.user = session.user
        except Session.DoesNotExist:
            request.session = None
            request.user = None

        response = self.get_response(request)
        return response
