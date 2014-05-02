#! /usr/bin/python

import re
import logging

import bottle
#from bottle import run, post, request, get
import settings
from model import User
from manager import ServerManager

TEMPLATE = 'template'
HELP_REGEX = re.compile("help")
MANAGE_REGEX = re.compile("manage")

manager = ServerManager()
app = application = bottle.Bottle()

@app.post('/'+settings.PUBLIC_URL)
def report():
    if bottle.request.query.get('key') != settings.KEY:
        raise Exception("Not Signed")

    sender = bottle.request.forms.get('Sender')
    try:
        user = User.get(email=sender)
    except User.DoesNotExist:
        logging.error("Invalid User: {0}".format(sender))
        return "Invalid User" if settings.DEBUG else None

    if not user.is_active:
        logging.error("Inactive User: {0}".format(sender))
        return "Inactive User" if settings.DEBUG else None

    subject = bottle.request.forms.get('Subject')

    # Help
    if HELP_REGEX.search(subject):
        response = manager.help(user)

    # Command
    elif MANAGE_REGEX.search(subject):
        response = manager.manage(user, bottle.request.forms.get('stripped-text'))

    # Report
    else:
        response = manager.add_task(user, bottle.request.forms.get('stripped-text'))

    if settings.DEBUG and response:
        return response


@app.get('/'+settings.PUBLIC_URL)
def showform():
    if settings.DEBUG:
        return manager.get_template(settings.Templates.TEST_FORM).render(key=settings.KEY, public_url=settings.PUBLIC_URL)

if __name__ == '__main__':
#    bottle.run(app=)
    bottle.run(app=app, **settings.SERVER)
