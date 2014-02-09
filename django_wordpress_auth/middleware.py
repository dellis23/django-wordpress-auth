from django.utils.functional import SimpleLazyObject

from . import get_wordpress_user


class WordpressAuthMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "django-wordpress-auth requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        request.wordpress_user = SimpleLazyObject(lambda: get_wordpress_user(request))
