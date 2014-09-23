#! /usr/bin/python
import logging
from datetime import datetime, timedelta
from itertools import ifilter, groupby

import settings
from model import User, Task
from library.template import Template
from library.mailclient import MailClient, Subjects


class Cron(object):
    def __init__(self, now=datetime.now()):
        self.now = now + timedelta(hours=(1 if settings.DST else 0))
        self.template = Template()
        self.mailclient = MailClient()
        self.failure = 'Failed to send email with subject "{}" to {}.'
        self.success = 'Sent email with subject "{}" to {}.\n'

    def job(self):
        users = User.select().where(User.is_active == True)
        for user in ifilter(lambda user: user.is_due(self.now), users):
            if self.send_email(user, self.create_digest, Subjects.DIGEST):
                self.update_last_sent(user)
                logging.info("Sent digest to {}".format(user.name))
        for user in ifilter(lambda user: user.is_late(self.now), users):
            if self.send_email(user, self.create_reminder, Subjects.REMINDER):
                self.update_last_reminded(user)
                logging.info("Sent reminder to {}".format(user.name))

    def send_email(self, user, create_email, subject):
        try:
            self.mailclient.send(user, create_email(user), subject)
            if settings.DEBUG:
                print self.success.format(subject, user.name)
            return True
        except Exception as e:
            logging.error(self.failure.format(subject, user.name))
            logging.error(e)
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
            'tasks': self.format_tasks(tasks, user),
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

    def format_tasks(self, all_tasks, recipient):
        formatted_tasks = []
        timezone = timedelta(hours=recipient.timezone)
        usergen = groupby(all_tasks, lambda task: task.user.name)
        for user, user_tasks in usergen:
            date_tasks = []
            dategen = groupby(
                user_tasks,
                lambda task: (task.date + timezone).strftime("%a %D, %Y")
            )
            for date, tasks in dategen:
                date_tasks.append({'date': date, 'tasks': [t.description for t in tasks]})
            formatted_tasks.append({'user': user, 'tasks': date_tasks})
        return formatted_tasks


# Cron for creating digest emails
if __name__ == '__main__':
    try:
        logging.info("{0} Starting cron {0}".format("=" * 14))
        cron = Cron()
        cron.job()
        logging.info("{0} Finished cron {0}".format("=" * 14))
    except Exception as e:
        logging.error(e)
        if settings.DEBUG:
            raise
