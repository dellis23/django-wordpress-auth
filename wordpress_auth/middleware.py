from django.utils.functional import SimpleLazyObject

from wordpress_auth.utils import get_wordpress_user


class WordPressAuthMiddleware(object):
    def process_request(self, request):
        request.wordpress_user = SimpleLazyObject(lambda: get_wordpress_user(request))

class WordPressRemoteUserMiddleware(object):
    def process_request(self, request):
        if request.wordpress_user:
            request.META['REMOTE_USER'] = request.wordpress_user.login
