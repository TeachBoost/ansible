#! /usr/bin/python
import bottle

import settings
from controller import admin as admin_controller
from controller import email as email_controller

app = application = bottle.Bottle()

# Base url for regular users
app.route(settings.BASEPATH, 'GET', admin_controller.index)
app.route(settings.BASEPATH + '/', 'GET', admin_controller.index)
app.route(
    settings.BASEPATH + '/tasks/<id>',
    'GET',
    admin_controller.read_user_tasks
)
app.route(
    settings.BASEPATH + '/update/<id>',
    'POST',
    admin_controller.update_self
)

# Email handler
email = bottle.Bottle()
app.mount(settings.EMAIL_PATH, email)
email.route('/', 'POST', email_controller.receive_email)
email.route('/', 'GET', email_controller.test_form)
email.route('', 'GET', email_controller.test_form)

# Ansible admin
admin = bottle.Bottle()
app.mount(settings.ADMIN_PATH, admin)
admin.route('/tasks', 'GET', admin_controller.read_tasks)
admin.route('/create', 'POST', admin_controller.create_person)
admin.route('/delete', 'POST', admin_controller.delete_people)
admin.route('/<id>', 'GET', admin_controller.read_person)
admin.route('/<id>', 'POST', admin_controller.update_person)
admin.route('/', 'GET', admin_controller.admin)

# Static files
app.route(
    settings.STATIC_PATH + '/<type>/<filename>',
    'GET',
    lambda **kwargs: bottle.static_file(
        filename=kwargs['filename'], root='static/' + kwargs['type']
    )
)

if __name__ == '__main__':
    bottle.run(app=app, reloader=True, **settings.SERVER)
