=====================
Django Wordpress Auth
=====================

Introduction
============

Allows for access in Django to a Wordpress installation for checking for 
things like login status and roles / capabilities.

Requirements
============

Python Dependencies :

 * `phpserialize`_

Wordpress Dependencies :

 * `root Cookie`_
 * `Members`_

 .. _`phpserialize`: http://pypi.python.org/pypi/phpserialize
 .. _`root Cookie`: http://wordpress.org/extend/plugins/root-cookie/
 .. _`Members`: http://wordpress.org/extend/plugins/members/

Installation
============

Add your wordpress's auth keys and salts (found in wp-config.php).

.. sourcecode:: python

    LOGGED_IN_KEY = "rs&^D%jPdu=vk|VVDsdfsdgsdgsdg9sd87f98s7h[Xm$3gT/@1xdasd"
    LOGGED_IN_SALT = "3]x^n{d8=su23902iu09jdc09asjd09asjd09jasdV-Lv-OydAQ%?~"

Add your wordpress database.

.. sourcecode:: python

    DATABASES = {
        'default': {
            ... # default django DB
        },
        'wordpress': {  # must be named 'wordpress'
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'wordpress',
            'USER': 'XXX',
            'PASSWORD': 'XXX',
            'HOST': '',
            'PORT': '',
        }
    }

Add the middleware.  Make sure it's placed somewhere after the session
middleware.

.. sourcecode:: python

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        # ...
        'django_wordpress_auth.middleware.WordpressAuthMiddleware',
    )

Finally, add to installed apps.

.. sourcecode:: python

    INSTALLED_APPS = (
        # ...
        'django_wordpress_auth',
    )

Usage
=====

To restrict a view to a certain role, simply wrap the view in the
``wordpress_requires_role`` decorator.

.. sourcecode:: python

    from django_wordpress_auth.decorators import wordpress_requires_role

    @wordpress_requires_role('my_role')
    def my_view():
        pass

You can restrict a view to a capability as well.

.. sourcecode:: python

    from django_wordpress_auth.decorators import wordpress_requires_capability

    @wordpress_requires_capability('my_capability')
    def my_view():
        pass

Finally, the middleware provides access to the wordpress user via
``request.wordpress_user``.

See ``models.py`` for full reference.  Some of the redundant naming conventions
in the wordpress database have been made simpler as well.
