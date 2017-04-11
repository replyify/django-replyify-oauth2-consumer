#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.crypto import get_random_string
from .models import Credentials
from . import settings
from datetime import timedelta
import requests


def index(request=None):
    return HttpResponse("Replyify-OAuth2 index.")


@login_required
def authorize(request=None):
    uid = getattr(request.user, settings.REPLYIFY_USER_ID_FIELD)
    client_id = settings.REPLYIFY_CLIENT_ID
    redirect_uri = settings.REPLYIFY_REDIRECT_URI
    response_type = 'code'

    state = get_random_string(20, "abcdefghijklmnopqrstuvwxyz0123456789")
    request.session['state'] = {state: uid}

    args = [
        "client_id={0}".format(client_id),
        "redirect_uri={0}".format(redirect_uri),
        "response_type={0}".format(response_type),
        "state={0}".format(state)
    ]
    url = "{0}?{1}".format(settings.REPLYIFY_AUTH_URL, "&".join(args))

    return redirect(url)


@login_required
def callback(request=None):
    if 'error' in request.GET:
        raise Exception(request.GET['error'])

    uid = _check_state(request)
    code = request.GET['code']
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': settings.REPLYIFY_CLIENT_ID,
        'redirect_uri': settings.REPLYIFY_REDIRECT_URI
    }
    url = settings.REPLYIFY_TOKEN_URL
    r = requests.post(url=url, data=data)
    data = r.json()
    creds = _store_credentials(uid, data)

    return HttpResponse(creds)


@login_required
def refresh(request=None):
    if 'error' in request.GET:
        raise Exception(request.GET['error'])

    try:
        creds = Credentials.objects.get(user=request.user)

        data = {
            'grant_type': 'refresh_token',
            'client_id': settings.REPLYIFY_CLIENT_ID,
            'client_secret': settings.REPLYIFY_CLIENT_SECRET,
            'refresh_token': creds.refresh_token
        }

        url = settings.REPLYIFY_TOKEN_URL
        r = requests.post(url=url, data=data)
        data = r.json()

        creds = _store_credentials(user=request.user, data=data)
        return HttpResponse(creds)

    except Credentials.DoesNotExist:
        authorize(request)


def _check_state(request=None):
    uid = getattr(request.user, settings.REPLYIFY_USER_ID_FIELD)
    msg = "Something fishy is happening. Abort ..."

    if 'state' not in request.session:
        raise Exception(msg)
    state = request.GET['state']
    from_session = request.session['state'][state]
    if from_session != uid:
        raise Exception(msg)

    request.session.pop('state')
    return uid


def _store_credentials(user, data=None):
    assert user is not None
    creds, _ = Credentials.objects.get_or_create(user=user)
    creds.access_token = data['access_token']
    creds.refresh_token = data['refresh_token']
    creds.expires = timezone.now() + timedelta(seconds=data['expires_in'])
    creds.scope = data['scope']
    creds.token_type = data['token_type']
    creds.save()
    return creds
