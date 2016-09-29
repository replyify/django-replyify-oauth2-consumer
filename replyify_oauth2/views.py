#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from datetime import timedelta

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.crypto import get_random_string

import _settings
from .models import Credentials


def index(request=None):
    return HttpResponse("Replyify-OAuth2 index.")


@login_required
def authorize(request=None):
    uid = _get_uid(request)
    client_id = _settings.REPLYIFY_CLIENT_ID
    redirect_uri = _settings.REPLYIFY_REDIRECT_URI
    response_type = 'code'

    state = get_random_string(20, "abcdefghijklmnopqrstuvwxyz0123456789")
    request.session['state'] = {state: uid}

    args = [
        "client_id={0}".format(client_id),
        "redirect_uri={0}".format(redirect_uri),
        "response_type={0}".format(response_type),
        "state={0}".format(state)
    ]
    url = "{0}?{1}".format(_settings.REPLYIFY_AUTH_URL, "&".join(args))

    return redirect(url)


@login_required
def callback(request=None):
    if 'error' in request.GET:
        raise Exception(request.GET['error'])

    uid = _check_state(request)
    data = _exchange_auth_code(request)
    creds = _store_credentials(uid, data)

    return HttpResponse(creds)


@login_required
def refresh(request=None):
    if 'error' in request.GET:
        raise Exception(request.GET['error'])

    uid = _get_uid(request)

    try:
        creds = Credentials.objects.get(uid=uid)

        data = {
            'grant_type': 'refresh_token',
            'client_id': _settings.REPLYIFY_CLIENT_ID,
            'client_secret': _settings.REPLYIFY_CLIENT_SECRET,
            'refresh_token': creds.refresh_token
        }

        url = _settings.REPLYIFY_TOKEN_URL
        r = requests.post(url=url, data=data)
        data = r.json()

        creds = _store_credentials(uid=uid, data=data)
        return HttpResponse(creds)

    except Credentials.DoesNotExist:
        authorize(request)


def _get_uid(request=None):
    if hasattr(request.user, 'guid'):
        uid = request.user.guid
    else:
        uid = request.user.id
    return uid


def _check_state(request=None):
    uid = _get_uid(request)
    msg = "Something fishy is happening. Abort ..."

    if 'state' not in request.session:
        raise Exception(msg)
    state = request.GET['state']
    from_session = request.session['state'][state]
    if from_session != uid:
        raise Exception(msg)

    request.session.pop('state')
    return uid


def _exchange_auth_code(request=None):
    code = request.GET['code']
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': _settings.REPLYIFY_CLIENT_ID,
        'redirect_uri': _settings.REPLYIFY_REDIRECT_URI
    }
    url = _settings.REPLYIFY_TOKEN_URL
    r = requests.post(url=url, data=data)
    return r.json()


def _store_credentials(uid=None, data=None):
    try:
        creds = Credentials.objects.get(uid=uid)
        creds.access_token = data['access_token']
        creds.refresh_token = data['refresh_token']
        creds.expires = timezone.now() + timedelta(seconds=data['expires_in'])
        creds.scope = data['scope']
        creds.token_type = data['token_type']
        creds.save()

    except Credentials.DoesNotExist:
        creds = Credentials.objects.create(
            uid=uid,
            access_token=data['access_token'],
            refresh_token=data['refresh_token'],
            expires=timezone.now() + timedelta(seconds=data['expires_in']),
            scope=data['scope'],
            token_type=data['token_type']
        )

    return creds
