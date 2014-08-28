import sys
from datetime import datetime, timedelta

from bottle import redirect, request, HTTPResponse

import settings
from model import User, Task
from library.template import Template
from library.auth import auth, admin_only, self_only, debug_only

template = Template()
ONE_WEEK = 7

@auth
def index(user):
    return template.render('index.tpl', user=user, title='Welcome')


@auth
@self_only
def update_self(id, user):
    user.update_schedule(request.forms)
    user.save()
    return redirect(settings.PUBLIC_URL)


@auth
@admin_only
def admin(user):
    ''' Show the admin page '''
    users = User.select().where(User.is_active==True)
    return template.render(
       'admin.tpl', users=users, title='Admin',
       email_url=(settings.EMAIL_URL if settings.DEBUG else None))


@auth
@admin_only
def create_person(user):
    name = request.forms.get('name')
    email = request.forms.get('email')
    if not name or not email:
        return redirect(settings.PUBLIC_URL)

    try:
        person = User.get(email=email)
        person.name = name
        person.is_active = True
        person.save()
    except:
        person = User.create(name=name, email=email)

    return redirect('{0}/admin/{1}'.format(settings.PUBLIC_URL, person.id))


@auth
@admin_only
def read_person(id, user):
    try:
        person = User.get(id=id)
    except:
        return redirect(settings.PUBLIC_URL)
    return template.render('read_person.tpl', person=person)


@auth
@admin_only
def update_person(id, user):
    try:
        person = User.get(id=id)
    except:
        return redirect(settings.PUBLIC_URL)

    person.is_admin = user.id == person.id or request.forms.get('is_admin', False)
    person.update_schedule(request.forms)
    person.save()

    return template.render('read_person.tpl', person=person)


@auth
@admin_only
def read_tasks(user):
    zero = {'hour': 0, 'minute': 0, 'second': 0, 'microsecond': 0}
    try:
        week = int(request.query.get('w', 0))
    except:
        week = 0
    current = datetime.now().replace(**zero) - timedelta(week * ONE_WEEK)
    start = current - timedelta(current.weekday())
    end = start + timedelta(ONE_WEEK)
    tasks = Task.select().where(Task.date > start, Task.date <= end)
    return template.render('read_tasks.tpl', tasks=tasks, start=start, week=week)


@auth
@admin_only
def delete_people(user):
    for id in request.forms:
        try:
            person = User.get(id=id)
            person.is_active = False
            person.save()
        except:
            pass
    return redirect(settings.PUBLIC_URL + '/admin')
