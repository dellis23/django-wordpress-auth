import hmac
import hashlib
import md5
import urllib2

from django.conf import settings
import phpserialize

from models import WpOptions, WpUsers, WpUsermeta


SITE_URL = WpOptions.objects.using('wordpress')\
          .get(option_name='siteurl').option_value
COOKIEHASH = md5.new(SITE_URL).hexdigest()
LOGIN_URL = SITE_URL + "/wp-login.php"


def _hmac(salt, data):
    return hmac.new(salt, msg=data, digestmod=hashlib.md5).hexdigest()


def _generate_auth_cookie(username, password, expires):
    expires = str(expires)
    wp_salt = settings.LOGGED_IN_KEY + settings.LOGGED_IN_SALT
    pass_fragment = password[8:12]
    wp_hash = _hmac(wp_salt, username + pass_fragment + "|" + expires)
    auth_cookie = _hmac(wp_hash, username + "|" + expires)
    return auth_cookie


def get_wordpress_user(request):
    cookie_key = 'wordpress_logged_in_' + COOKIEHASH
    cookie_value = request.COOKIES.get(cookie_key)
    if not cookie_value:
        return None
    username, expires, hmac = urllib2.unquote(cookie_value).split('|')
    wp_user = WpUsers.objects.using('wordpress').get(login=username)
    if hmac == _generate_auth_cookie(username, wp_user.password, expires):
        return wp_user
    else:
        return None
