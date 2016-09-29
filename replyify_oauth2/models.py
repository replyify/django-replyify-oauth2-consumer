#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class Credentials(models.Model):
    uid = models.CharField(max_length=50)
    access_token = models.CharField(max_length=50)
    refresh_token = models.CharField(max_length=50)
    expires = models.DateTimeField(default=timezone.now)
    scope = models.CharField(max_length=50)
    token_type = models.CharField(max_length=50)

    def expired(self):
        if timezone.now() > self.expires:
            return True
        return False
