#! /usr/bin/python
import re
import logging
from itertools import ifilter

import bottle

import settings
from model import User
from manager import ServerManager, AdminManager

HELP_REGEX = re.compile("help")
MANAGE_REGEX = re.compile("manage")
SUBSCRIPTION_REGEX = re.compile("subscriptions")

manager = ServerManager()
admin_manager = AdminManager()

app = application = bottle.Bottle()
ansible = bottle.Bottle()
app.mount(settings.PUBLIC_URL, ansible)

@app.post(settings.PUBLIC_URL + '/email/')
def report():
    if bottle.request.query.get('key') != settings.KEY:
        raise Exception("Not Signed")

    sender = bottle.request.forms.get('Sender', bottle.request.forms.get('sender') )
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

    # Subscriptions
    elif SUBSCRIPTION_REGEX.search(subject):
        response = manager.show_subscriptions(user)

    # Report
    else:
        response = manager.add_task(user, bottle.request.forms.get('stripped-text'))

    if settings.DEBUG and response:
        return response

@app.get(settings.PUBLIC_URL + '/email/')
def showform():
    if settings.DEBUG:
        template = manager.get_template(settings.Templates.TEST_FORM)
        template_vars = {'key': settings.KEY, 'basepath': settings.BASEPATH}
        return template.render(**template_vars)

@ansible.get('/admin/<id>')
def user_admin(id):
    try:
        user = User.get(id=id)
    except:
        return bottle.redirect(settings.PUBLIC_URL+ '/admin')
    return admin_manager.user_template.render(user=user, basepath=settings.BASEPATH)

@ansible.post('/admin/<id>')
def user_update(id):
    admin_manager.update(id, bottle.request.forms)
    return user_admin(id)

@ansible.get('/admin/')
def all_admin():
    users = User.select().where(User.is_active==True)
    response = admin_manager.all_template.render(users=users, basepath=settings.BASEPATH)
    return response

@ansible.post('/admin/delete')
def admin_delete():
    inputs = bottle.request.forms
    ids = ifilter(lambda field: inputs[field], inputs)
    [admin_manager.remove(user_id) for user_id in ids]
    return bottle.redirect(settings.PUBLIC_URL + '/admin')

@ansible.post('/admin/add')
def admin_add():
    inputs = bottle.request.forms
    admin_manager.create(inputs.get('name'), inputs.get('email'))
    return bottle.redirect(settings.PUBLIC_URL + '/admin')

if __name__ == '__main__':
    bottle.run(app=app, **settings.SERVER)
