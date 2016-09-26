#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from django.contrib import admin
from .models import ReplyifyOAuthCredentials

admin.site.register(ReplyifyOAuthCredentials)
