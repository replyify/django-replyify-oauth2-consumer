#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
import _settings


def index(request):
    return HttpResponse("Replyify-OAuth2 index.")


def authorize(request):
    client_id = _settings.REPLYIFY_CLIENT_ID
    redirect_uri = _settings.REPLYIFY_REDIRECT_URI
    response_type = 'code'
    state = get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")

    args = "client_id={0}&redirect_uri={1}&response_type={2}&state={3}".format(client_id, redirect_uri, response_type, state)
    url = "{0}?{1}".format(_settings.REPLYIFY_AUTH_URL, args)

    return redirect(url)


def callback(request):
    return HttpResponse(str(request))
