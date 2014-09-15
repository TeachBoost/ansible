#! /usr/bin/python
import logging
from datetime import datetime, timedelta
from itertools import ifilter

import settings
from model import User, Task
from library.template import Template
from library.mailclient import MailClient, Subjects


class Cron(object):
    def __init__(self, now):
        self.now = now
        self.template = Template()
        self.mailclient = MailClient()
        self.failure = "Failed to send email with subject {} to {}."
        self.success = "Sent email with subject {} to {}.\n"

    def job(self):
        users = User.select().where(User.is_active == True)
        for user in ifilter(lambda user: user.is_due(self.now), users):
            self.send_email(user, self.create_digest, Subjects.DIGEST)
            self.update_last_sent(user)
        for user in ifilter(lambda user: user.is_late(self.now), users):
            self.send_email(user, self.create_reminder, Subjects.REMINDER)
            self.update_last_reminded(user)

    def send_email(self, user, create_email, subject):
        try:
            self.mailclient.send(user, create_email(user), subject)
            if settings.DEBUG:
                print self.success.format(subject, user.name)
        except:
            logging.error(self.failure.format(subject, user.name))
            if settings.DEBUG:
                raise

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
            'sender': settings.SENDER,
            'timezone_correct': timedelta(hours=user.timezone)
        }
        return self.template.render('email_digest.tpl', **email_params)

    def create_reminder(self, user):
        return self.template.render('email_reminder.tpl', user=user)

    def update_last_sent(self, user):
        if not settings.DEBUG:
            user.last_sent = self.now
            user.save()

    def update_last_reminded(self, user):
        if not settings.DEBUG:
            user.last_reminded = self.now
            user.save()


# Cron for creating digest emails
if __name__ == '__main__':
    try:
        cron = Cron(datetime.now())
        cron.job()
    except Exception as e:
        logging.error(e)
        if settings.DEBUG:
            raise
