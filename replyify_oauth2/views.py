#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
import _settings


def index(request):
    return HttpResponse("Replyify-OAuth2 index.")


@login_required
def authorize(request):
    uid = request.user.guid
    client_id = settings.REPLYIFY_CLIENT_ID
    redirect_uri = settings.REPLYIFY_REDIRECT_URI
    response_type = 'code'

    # TODO(froch): store state in redis with user.id
    state = get_random_string(20, "abcdefghijklmnopqrstuvwxyz0123456789")

    args = "client_id={0}&redirect_uri={1}&response_type={2}&state={3}".format(client_id, redirect_uri, response_type, state)
    url = "{0}?{1}".format(settings.REPLYIFY_AUTH_URL, args)

    return redirect(url)


def callback(request):

    # TODO(froch): validate state with one saved above.
    state = request.GET['state']

    code = request.GET['code']
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': settings.REPLYIFY_CLIENT_ID,
        'redirect_uri': settings.REPLYIFY_REDIRECT_URI
    }

    url = settings.REPLYIFY_TOKEN_URL
    r = requests.post(url=url, data=data)

    return HttpResponse(str(request))
