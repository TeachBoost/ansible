#! /usr/bin/python

import re
import logging

from bottle import run, post, request, get
import settings
from model import User
from manager import ServerManager

TEMPLATE = 'template'
HELP_REGEX = re.compile("help")
MANAGE_REGEX = re.compile("manage")

manager = ServerManager()

@post('/')
def report():
    if request.forms.get('key') != settings.KEY:
        raise Exception("Not Signed")
    try:
        user = User.get(email=request.forms.get('from'))
    except User.DoesNotExist:
        logging.error("Invalid User: {0}".format(request.forms.get('from')))
        return

    if not user.is_active:
        logging.error("Inactive User: {0}".format(request.forms.get('from')))
        return

    subject = request.forms.get('subject')

    # Help
    if HELP_REGEX.search(subject):
        response = manager.help(user)

    # Command
    elif MANAGE_REGEX.search(subject):
        response = manager.manage(user, request.forms.get('body'))

    # Report
    else:
        response = manager.add_task(user, request.forms.get('body'))

    if settings.DEBUG and response:
        return response


@get('/')
def showform():
    if settings.DEBUG:
        return manager.get_template(settings.Templates.TEST_FORM).render(key=settings.KEY)

run(**settings.SERVER)

