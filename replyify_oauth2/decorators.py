#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from functools import wraps
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .models import Credentials


def replyify_auth_required(func):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            try:
                if Credentials.objects.get(user=request.user).is_valid():
                    return func(request, *args, **kwargs)
            except Credentials.DoesNotExsit:
                return redirect(reverse('replyfy:authorize') + '?next=' + request.GET.get('next', request.path))
            return redirect(reverse('replyfy:refresh') + '?next=' + request.GET.get('next', request.path))
        return wraps(func)(inner_decorator)
    return decorator(func)