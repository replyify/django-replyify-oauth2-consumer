#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from __future__ import unicode_literals
from django.db import models


class ReplyifyOAuthCredentials(models.Model):
    access_token = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=50)
    expires = models.DateTimeField(auto_now=True)
