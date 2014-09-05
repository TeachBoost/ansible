import logging

from bottle import HTTPResponse, request

import settings
from model import User


def auth(function):
    def decorate(*args, **kwargs):
        serial = request.environ.get('SERIAL')
        verified = request.environ.get('VERIFIED') == 'SUCCESS'
        if settings.DEBUG:
            verified = True
            serial = serial or '06'
        if not (serial and verified):
            return forbidden()
        try:
            user = User.get(serial=serial)
        except:
            user = None
        if not (user and user.is_active):
            return forbidden()
        else:
            kwargs['user'] = user
            return function(*args, **kwargs)
    return decorate


def admin_only(function):
    def decorate(*args, **kwargs):
        if getattr(kwargs.get('user'), 'is_admin', False):
            return function(*args, **kwargs)
        else:
            return forbidden()
    return decorate


def self_only(function):
    def decorate(*args, **kwargs):
        try:
            id = int(kwargs['id'])
        except:
            return bad_request()

        if id == getattr(kwargs.get('user'), 'id', 0):
            return function(*args, **kwargs)
        else:
            return forbidden()
    return decorate


def debug_only(function):
    def decorate(*args, **kwargs):
        'checking debug'
        if settings.DEBUG:
            return function(*args, **kwargs)
        else:
            return forbidden()
    return decorate


def auth_email(function):
    def decorate(*args, **kwargs):
        if request.query.get('key') != settings.KEY:
            return forbidden()
        sender = request.forms.get('Sender', request.forms.get('sender'))
        try:
            user = User.get(email=sender)
        except:
            return forbidden()
        kwargs['user'] = user
        return function(*args, **kwargs)
    return decorate


def forbidden(text=''):
    return HTTPResponse(status=403, body="403: Forbidden -- " + text)


def bad_request():
    return HTTPResponse(status=400, body="400: Bad Request")
