from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from wordpress_auth.utils import get_login_url

def _redirect_to_login(request):
    redirect_to = request.build_absolute_uri(request.path)
    return redirect(get_login_url() + "?redirect_to=" + redirect_to)


def wordpress_login_required(fn, *args, **kwargs):
    def wrapped(request, *args, **kwargs):
        if not request.wordpress_user:
            return _redirect_to_login(request)
        else:
            return fn(request, *args, **kwargs)
    return wrapped


def wordpress_requires_role(role):
    def real_decorator(fn, *args, **kwargs):
        def wrapped(request, *args, **kwargs):

            if not request.wordpress_user:
                return _redirect_to_login(request)

            if role in request.wordpress_user.roles:
                return fn(request, *args, **kwargs)
            else:
                raise PermissionDenied()

        return wrapped
    return real_decorator


def wordpress_requires_capability(capability):
    def real_decorator(fn, *args, **kwargs):
        def wrapped(request, *args, **kwargs):

            if not request.wordpress_user:
                return _redirect_to_login(request)

            if capability in request.wordpress_user.capabilities:
                return fn(request, *args, **kwargs)
            else:
                raise PermissionDenied()

        return wrapped
    return real_decorator
