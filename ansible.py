#! /usr/bin/python
import bottle

import settings
from controller import admin as admin_controller
from controller import email as email_controller

app = application = bottle.Bottle()

# Email handler
email = bottle.Bottle()
app.mount(settings.EMAIL_URL, email)
email.route('/', 'POST', email_controller.receive_email)
email.route('/', 'GET', email_controller.test_form)
email.route('', 'GET', email_controller.test_form)

# Ansible admin 
admin = bottle.Bottle()
app.mount(settings.PUBLIC_URL, admin)
admin.route('/update/<id>', 'POST', admin_controller.update_self)
admin.route('/admin/tasks', 'GET', admin_controller.read_tasks)
admin.route('/admin/create', 'POST', admin_controller.create_person)
admin.route('/admin/delete', 'POST', admin_controller.delete_people)
admin.route('/admin/<id>', 'GET', admin_controller.read_person)
admin.route('/admin/<id>', 'POST', admin_controller.update_person)
admin.route('/admin', 'GET', admin_controller.admin)
admin.route('/', 'GET', admin_controller.index)
admin.route('', 'GET', admin_controller.index)


if __name__ == '__main__':
    bottle.run(app=app, reloader=True, **settings.SERVER)
