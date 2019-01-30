import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        if not request.user.is_authenticated:
            if not any(url.match(path) for url in EXEMPT_URLS):
                login_url = settings.LOGIN_URL
                if len(path) > 0 and is_safe_url(
                        url=request.path_info, allowed_hosts=request.get_host()):
                    # Add 'next' GET variable to support
                    # redirection after login
                    login_url = '{}?next={}'.format(settings.LOGIN_URL, request.path_info)

                return HttpResponseRedirect(login_url)

        return None
