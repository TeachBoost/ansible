from datetime import datetime, timedelta
from calendar import day_abbr as DAYS
import logging

from peewee import SqliteDatabase, CharField, ForeignKeyField, \
    DateTimeField, TextField, IntegerField, Model, BooleanField, \
    FloatField

import settings


db = SqliteDatabase(settings.DATABASE)
zero_minutes = {'minute': 0, 'second': 0, 'microsecond': 0}
ONE_DAY = timedelta(1)
NEVER = datetime.fromtimestamp(0)


############################################
# For now there's only one model file, but #
# if there are going to be more classes or #
# more functionality on existing models we #
# should really consider creating separate #
# model files for each defined model class #
############################################


class User(Model):
    class Meta:
        database = db

    name = CharField()
    email = CharField(index=True, unique=True)
    serial = CharField(index=True, unique=True)
    timezone = FloatField(default=-5.0)  # Eastern
    send_reminders = BooleanField(default=True, null=True)
    is_admin = BooleanField(default=False, null=True)
    is_active = BooleanField(default=True)
    Mon = IntegerField(null=True)
    Tue = IntegerField(null=True)
    Wed = IntegerField(null=True)
    Thu = IntegerField(null=True)
    Fri = IntegerField(null=True)
    Sat = IntegerField(null=True)
    Sun = IntegerField(null=True)
    last_sent = DateTimeField(null=True)
    last_reminded = DateTimeField(null=True)
    created = DateTimeField(default=datetime.now)

    def is_due(self, date):
        '''
        Determines if a user is due to recieve a digest email
        A user is due if:
            they have a subscription for the current day
            it is past the time of their subscription
            the last email was sent before today's subscription time
        '''
        subscription_hour = getattr(self, date.strftime("%a"), None)
        if subscription_hour is None:
            logging.info("{} has no subscription for today".format(self.name))
            return

        subscription_hour = int(subscription_hour + self.timezone)
        last_sent = self.last_sent or NEVER
        subscription = date.replace(hour=subscription_hour, **zero_minutes)
        subscription -= timedelta(hours=self.timezone)
        due = date >= subscription and last_sent < subscription
        if not due:
            logging.debug("Skipping {}'s digest".format(self.name))
            logging.debug("    subscription: {}".format(
                subscription.strftime("%c")
            ))
            logging.debug("    last message: {}".format(
                last_sent.strftime("%c")
            ))
        else:
            logging.info("{} is due".format(self.name))
        return due

    def is_late(self, date):
        '''
        Determines if a user is late sending their task email for the day and
        should be reminded. Uses the deadline defined in settings.REPORT_DUE
        A user should be reminded if:
            it is past the deadline for reporting
            they have not emailed for 24 hours before the deadline
            they have not already been sent a reminder in the last 24 hours
            they are configured to receive reminders
            it is not a weekend
        '''
        last_reminded = self.last_reminded or NEVER
        deadline = date.replace(hour=settings.REPORT_DUE, **zero_minutes)
        try:
            last_task = Task.select(Task.date).where(Task.user == self)\
                .order_by(Task.date.desc()).get()
            last_reported = last_task.date
        except:
            last_reported = NEVER

        late = all([
            date >= deadline,
            deadline - last_reported > ONE_DAY,
            date - last_reminded > ONE_DAY,
            self.send_reminders,
            date.strftime('%a') not in ['Sat', 'Sun'],
        ])

        if not late:
            logging.debug("Skipping {}'s reminder".format(self.name))
            logging.debug("    deadline: {}".format(deadline.strftime("%c")))
            logging.debug("    last_reminded: {}".format(
                last_reminded.strftime("%c")
            ))
            logging.debug("    last_reported: {}".format(
                last_reported.strftime("%c")
            ))
            logging.debug("    send_reminders: {}".format(
                self.send_reminders
            ))
        else:
            logging.info("{} is late".format(self.name))
        return late

    def update_last_sent(self, time):
        '''
        Updates the last_sent property of a user
        time = the time to save as last_sent
        '''
        self.last_sent = time
        self.save()

    def update_schedule(self, schedule):
        '''
        Updates a user's email schedule
        schedule = an object with day attributes
        and time values
        '''
        for day in DAYS:
            time = schedule.get(day)
            try:
                time = int(time)
                if time < 0 or time >= 24:
                    time = None
                else:
                    time = int(time - self.timezone)
            except:
                time = None
            setattr(self, day, time)
        return self


class Task(Model):
    class Meta:
        database = db

    user = ForeignKeyField(User)
    date = DateTimeField(default=datetime.now)
    description = TextField()
