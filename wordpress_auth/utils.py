import hmac
import hashlib
from time import time

from django.utils.six.moves.urllib.parse import urljoin, unquote_plus
from django.utils.encoding import force_bytes

from wordpress_auth import (WORDPRESS_LOGGED_IN_KEY, WORDPRESS_LOGGED_IN_SALT,
                            WORDPRESS_COOKIEHASH)
from wordpress_auth.models import WpOptions, WpUsers


def get_site_url():
    url = WpOptions.objects.using('wordpress') \
        .get(option_name='siteurl').option_value

    return _untrailingslashit(url)


def get_login_url():
    return urljoin(get_site_url(), 'wp-login.php')


def get_wordpress_user(request):
    if WORDPRESS_COOKIEHASH is None:
        cookie_hash = hashlib.md5(force_bytes(get_site_url())).hexdigest()
    else:
        cookie_hash = WORDPRESS_COOKIEHASH

    cookie = request.COOKIES.get('wordpress_logged_in_' + cookie_hash)

    if cookie:
        cookie = unquote_plus(cookie)
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
    key = hmac.new(force_bytes(key_salt), force_bytes(key_msg),
        digestmod=hashlib.md5).hexdigest()

    hash_msg = '{}|{}|{}'.format(username, expiration, token)
    hash = hmac.new(force_bytes(key), force_bytes(hash_msg),
        digestmod=hashlib.sha256).hexdigest()

    if hash != cookie_hmac:
        return False

    # *sigh* we're almost there
    # Check if the token is valid for the given user
    verifier = hashlib.sha256(force_bytes(token)).hexdigest()

    if verifier not in user.get_session_tokens():
        return False

    return user
