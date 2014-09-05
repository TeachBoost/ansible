from datetime import datetime, timedelta

from bottle import redirect, request
from peewee import IntegrityError

import settings
from model import User, Task
from library.template import Template
from library.auth import auth, admin_only, self_only

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
    return redirect(settings.BASEPATH)


@auth
@admin_only
def admin(user):
    ''' Show the admin page '''
    users = User.select().where(User.is_active == True).order_by(User.name)
    print users
    return template.render(
        'admin.tpl',
        users=users,
        title='Admin',
        user=user,
        email_url=(settings.EMAIL_PATH if settings.DEBUG else None)
    )


@auth
@admin_only
def create_person(user):
    name = request.forms.get('name')
    email = request.forms.get('email')
    serial = request.forms.get('serial')
    if not any([name, email, serial]):
        return redirect(settings.ADMIN_PATH)

    try:
        person = User.get(email=email)
    except:
        person = User()
        person.email = email
    person.name = name
    person.serial = serial
    person.is_active = True

    try:
        person.save()
    except IntegrityError:
        return redirect(settings.ADMIN_PATH)

    return redirect('{0}/{1}'.format(settings.ADMIN_PATH, person.id))


@auth
@admin_only
def read_person(id, user):
    try:
        person = User.get(id=id)
    except:
        return redirect(settings.ADMIN_PATH)
    return template.render('read_person.tpl', person=person, user=user)


@auth
@admin_only
def update_person(id, user):
    try:
        person = User.get(id=id)
    except:
        return redirect(settings.ADMIN_PATH)

    person.is_admin = user.id == person.id \
        or request.forms.get('is_admin', False)
    person.serial = request.forms.get('serial')
    person.email = request.forms.get('email')
    person.update_schedule(request.forms)

    try:
        person.save()
    except IntegrityError:
        person = User.get(id=id)

    return template.render('read_person.tpl', person=person, user=user)


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
    return template.render(
        'read_tasks.tpl',
        tasks=tasks,
        start=start,
        week=week,
        user=user
    )


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
    return redirect(settings.ADMIN_PATH)
