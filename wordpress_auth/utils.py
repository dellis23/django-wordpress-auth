import hmac
import hashlib

try:
    from urllib.parse import urljoin, unquote
except ImportError:
    from urlparse import urljoin  # Python 2
    from urllib2 import unquote

from wordpress_auth import WORDPRESS_LOGGED_IN_KEY, WORDPRESS_LOGGED_IN_SALT
from wordpress_auth.models import WpOptions, WpUsers


def get_site_url():
    url = WpOptions.objects.using('wordpress') \
        .get(option_name='siteurl').option_value

    return _untrailingslashit(url)


def get_login_url():
    return urljoin(get_site_url(), 'wp-login.php')


def get_wordpress_user(request):
    cookie_hash = hashlib.md5(get_site_url().encode()).hexdigest()
    cookie = request.COOKIES.get('wordpress_logged_in_' + cookie_hash)

    if cookie:
        username, expires, hmac = unquote(cookie).split('|')
        user = WpUsers.objects.using('wordpress').get(login=username)

        if hmac == _generate_auth_cookie(username, user.password, expires):
            return user


def _untrailingslashit(str):
    return str.rstrip('/\\')


def _hmac(*args, **kwargs):
    kwargs['digestmod'] = hashlib.md5
    return hmac.new(*args, **kwargs).hexdigest()


def _generate_auth_cookie(username, password, expires):
    wp_salt = WORDPRESS_LOGGED_IN_KEY + WORDPRESS_LOGGED_IN_SALT
    wp_hash = _hmac(wp_salt, username + password[8:12] + "|" + expires)
    cookie = _hmac(wp_hash, username + "|" + expires)

    return cookie
