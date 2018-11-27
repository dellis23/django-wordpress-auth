__version__ = '0.1.31'

from django.conf import settings

WORDPRESS_TABLE_PREFIX = getattr(settings, 'WORDPRESS_TABLE_PREFIX', 'wp_')
WORDPRESS_LOGGED_IN_KEY = getattr(settings, 'WORDPRESS_LOGGED_IN_KEY')
WORDPRESS_LOGGED_IN_SALT = getattr(settings, 'WORDPRESS_LOGGED_IN_SALT')
WORDPRESS_COOKIEHASH = getattr(settings, 'WORDPRESS_COOKIEHASH', None)
