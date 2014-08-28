from bottle import HTTPResponse, request

import settings
from model import User


def auth(function):
    def decorate(*args, **kwargs):
        email = 'josh@teachboost.com'
        try:
            user = User.get(email=email)
        except:
            return forbidden()
        if not user.is_active:
            return forbidden()
        kwargs['user'] = user
        return function(*args, **kwargs)
    return decorate


@auth
def admin_only(function, user):
    def decorate(*args, **kwargs):
        if user.is_admin:
            return function(*args, **kwargs)
        else:
            return forbidden()
    return decorate


@auth
def admin_only_with_user(function, user):
    def decorate(*args, **kwargs):
        kwargs['user'] = user
        if user.is_admin:
            return function(*args, **kwargs)
        else:
            return forbidden()
    return decorate


@auth
def self_only(function, user):
    def decorate(*args, **kwargs):
        try:
            id = int(kwargs['id'])
        except:
            return bad_request()

        if id == user.id:
            kwargs['user'] = user
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
            print 'bad key'
            return forbidden()
        sender = request.forms.get('Sender', request.forms.get('sender'))
        print "sender:", sender
        try:
            user = User.get(email=sender)
        except:
            print 'bad sender'
            return forbidden()
        kwargs['user'] = user
        return function(*args, **kwargs)
    return decorate


def forbidden():
    return HTTPResponse(status=403, body="403: Forbidden")


def bad_request():
    return HTTPResponse(status=400, body="400: Bad Request")
