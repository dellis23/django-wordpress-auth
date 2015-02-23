=====================
Django WordPress Auth
=====================

Introduction
============

Allows for access in Django to a WordPress installation for checking for
things like login status and roles / capabilities.

Requirements
============

Python Dependencies:

 * `phpserialize`_

WordPress Dependencies:

 * `root Cookie`_
 * `Members`_

 .. _`phpserialize`: http://pypi.python.org/pypi/phpserialize
 .. _`root Cookie`: http://wordpress.org/extend/plugins/root-cookie/
 .. _`Members`: http://wordpress.org/extend/plugins/members/

Installation
============

Add your WordPress's auth keys and salts (found in wp-config.php) to your settings.py.

.. sourcecode:: python

    WORDPRESS_LOGGED_IN_KEY = "rs&^D%jPdu=vk|VVDsdfsdgsdgsdg9sd87f98s7h[Xm$3gT/@1xdasd"
    WORDPRESS_LOGGED_IN_SALT = "3]x^n{d8=su23902iu09jdc09asjd09asjd09jasdV-Lv-OydAQ%?~"

Add your WordPress database to DATABASES in settings.py.

.. sourcecode:: python

    DATABASES = {
        'default': {
            ... # default django DB
        },
        'wordpress': {  # must be named 'wordpress'
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'wordpress',
            'USER': '...',
            'PASSWORD': '...',
            'HOST': '...',
            'PORT': 3306,
        }
    }

Add the middleware to MIDDLEWARE_CLASSES in settings.py.
Make sure it's placed somewhere after the session middleware.

.. sourcecode:: python

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        # ...
        'wordpress_auth.middleware.WordPressAuthMiddleware',
    )

Finally, add `wordpress_auth` to INSTALLED_APPS.

.. sourcecode:: python

    INSTALLED_APPS = (
        # ...
        'wordpress_auth',
    )

Usage
=====

To restrict a view to a certain role, simply wrap the view in the
``wordpress_requires_role`` decorator.

.. sourcecode:: python

    from wordpress_auth.decorators import wordpress_requires_role

    @wordpress_requires_role('my_role')
    def my_view():
        pass

You can restrict a view to a capability as well.

.. sourcecode:: python

    from wordpress_auth.decorators import wordpress_requires_capability

    @wordpress_requires_capability('my_capability')
    def my_view():
        pass

Finally, the middleware provides access to the WordPress user via ``request.wordpress_user``.

See ``models.py`` for full reference.  Some of the redundant naming conventions
in the WordPress database have been made simpler as well.
