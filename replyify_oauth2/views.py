#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


from django.http import HttpResponse


def index(request):
    return HttpResponse("Replyify-OAuth2 index.")
