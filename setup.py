#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# See https://github.com/pybuilder/pybuilder/issues/56
del os.link


def version():
    with open(os.path.abspath(__file__).replace('setup.py', 'VERSION'), 'r') as v:
        return v.read()

setup(
    name='replyify-oauth2',
    version=version(),
    description='Replyify OAuth2 consumer for Django.',
    author='Replyify',
    author_email='team@replyify.com',
    url='http://github.com/replyify/django-replyify-oauth2-consumer',
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
        'Django>=1.6'
        'requests>=0.8.8'
    ],
    scripts=[],
    include_package_data=True,
    zip_safe=False
)
