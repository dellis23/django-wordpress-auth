#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-wordpress-auth',
    version='0.1.0',
    description='Django integration with WordPress authentication and roles / capabilities system.',
    long_description=open('README.rst').read(),
    include_package_data=True,
    packages=[
        'wordpress_auth',
    ],
    install_requires=[
        'Django',
        'phpserialize==1.3'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
