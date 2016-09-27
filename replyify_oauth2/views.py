#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import os
import redis
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.crypto import get_random_string

import _settings


def index(request):
    return HttpResponse("Replyify-OAuth2 index.")


def _get_uid(request=None):
    if hasattr('guid', request.user):
        uid = request.user.guid
    else:
        uid = request.user.id
    return uid


def _get_redis_connection(host=None, port=None, passwd=None):
    if not (host and port):
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        tokenized = redis_url.split(':')
        host = tokenized[1].lstrip('//')
        port = tokenized[2]
    try:
        r = redis.Redis(
            host=host,
            port=port,
            password=passwd
        )
        return r
    except:
        return None


@login_required
def authorize(request):
    uid = _get_uid(request)
    client_id = _settings.REPLYIFY_CLIENT_ID
    redirect_uri = _settings.REPLYIFY_REDIRECT_URI
    response_type = 'code'

    state = get_random_string(20, "abcdefghijklmnopqrstuvwxyz0123456789")
    r = _get_redis_connection()
    if r is not None:
        r.set(state, uid)

    args = "client_id={0}&redirect_uri={1}&response_type={2}&state={3}".format(client_id, redirect_uri, response_type, state)
    url = "{0}?{1}".format(_settings.REPLYIFY_AUTH_URL, args)

    return redirect(url)


def callback(request):
    uid = _get_uid(request)

    state = request.GET['state']
    r = _get_redis_connection()
    if r is not None:
        from_redis = r.get(state)
        if from_redis != uid:
            raise Exception("Something fishy is happening. Abort ...")

    code = request.GET['code']
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': _settings.REPLYIFY_CLIENT_ID,
        'redirect_uri': _settings.REPLYIFY_REDIRECT_URI
    }

    url = _settings.REPLYIFY_TOKEN_URL
    r = requests.post(url=url, data=data)

    return HttpResponse(str(request))
