#! /usr/bin/python
import logging
from datetime import datetime
from itertools import ifilter

import settings
from model import User, Task
from library.template import Template
from library.mailclient import MailClient, Subjects


class Cron(object):
    def __init__(self):
        self.now = datetime.now()
        self.template = Template()
        self.mailclient = MailClient()

    def job(self):
        users = User.select().where(User.is_active == True)
        for user in ifilter(lambda user: user.is_due(self.now), users):
            self.send_digest(user)
        for user in ifilter(lambda user: user.needs_reminding(self.now), users):
            self.send_reminder(user)


    def send_reminder(self, user):
        print "Reminding {0}".format(user.name)

    def send_digest(self, user):
            try:
                digest = self.create_digest(user)
                email = self.mailclient.send(user, digest, Subjects.DIGEST)
            except:
                logging.error("Failed to send email to {0}".format(user.name))
                if settings.DEBUG:
                    raise

            if settings.DEBUG:
                print user.name
                print email, '\n\n'
            else:
                user.last_sent = self.now
                user.save()

    def create_digest(self, user):
        last_sent = user.last_sent or user.created
        tasks = Task.select()\
            .where((Task.date > last_sent))\
            .order_by(Task.user.name, Task.date)
        email_params = {
            'user': user,
            'start': last_sent,
            'end': self.now,
            'tasks': tasks,
            'sender': settings.SENDER
        }
        return self.template.render('email_digest.tpl', **email_params)


# Cron for creating digest emails
if __name__ == '__main__':
    try:
        cron = Cron()
        cron.job()
    except Exception as e:
        logging.error(e)
        if settings.DEBUG:
            raise
