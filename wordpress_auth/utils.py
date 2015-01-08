import hmac
import hashlib
from time import time

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
        cookie = unquote(cookie)
        return _validate_auth_cookie(cookie)


def _untrailingslashit(str):
    return str.rstrip('/\\')


def _parse_auth_cookie(cookie):
    elements = cookie.split('|')
    return elements if len(elements) == 4 else None


def _validate_auth_cookie(cookie):
    cookie_elements = _parse_auth_cookie(cookie)

    if not cookie_elements:
        return False

    username, expiration, token, cookie_hmac = cookie_elements

    # Quick check to see if an honest cookie has expired
    if float(expiration) < time():
        return False

    # Check if a bad username was entered in the user authentication process
    try:
        user = WpUsers.objects.using('wordpress').get(login=username)
    except WpUsers.DoesNotExist:
        return False

    # Check if a bad authentication cookie hash was encountered
    pwd_frag = user.password[8:12]
    key_salt = WORDPRESS_LOGGED_IN_KEY + WORDPRESS_LOGGED_IN_SALT
    key_msg = '{}|{}|{}|{}'.format(username, pwd_frag, expiration, token)
    key = hmac.new(key_salt.encode(), key_msg.encode(), digestmod=hashlib.md5) \
        .hexdigest()

    hash_msg = '{}|{}|{}'.format(username, expiration, token)
    hash = hmac.new(key.encode(), hash_msg.encode(), digestmod=hashlib.sha256) \
        .hexdigest()

    if hash != cookie_hmac:
        return False

    # *sigh* we're almost there
    # Check if the token is valid for the given user
    verifier = hashlib.sha256(token.encode()).hexdigest().encode()

    if verifier not in user.get_session_tokens():
        return False

    return user
