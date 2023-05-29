from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin

from wordpress_auth.utils import get_wordpress_user


class WordPressAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.wordpress_user = SimpleLazyObject(lambda: get_wordpress_user(request))
