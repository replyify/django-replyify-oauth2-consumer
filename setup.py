#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# See https://github.com/pybuilder/pybuilder/issues/56
del os.link


with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as v:
    VERSION = v.read()


with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as readme:
    README = readme.read()


setup(
    name='django-replyify-oauth2',
    version=VERSION,
    description='Replyify OAuth2 consumer for Django',
    long_description=README,
    long_description_content_type='text/x-rst',
    author='Replyify',
    author_email='team@replyify.com',
    url='https://replyify.com',
    keywords=[
        'replyify',
        'oauth2',
        'django'
    ],
    packages=[
        'replyify_oauth2',
        'replyify_oauth2.migrations',
    ],
    install_requires=[
        'Django>=2.0',
        'requests>=0.10.1',
    ],
    scripts=[],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires='~=3.0',
)
