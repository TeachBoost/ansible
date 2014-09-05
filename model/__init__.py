from datetime import datetime
from calendar import day_abbr as DAYS

from peewee import SqliteDatabase, CharField, ForeignKeyField, \
    DateTimeField, TextField, IntegerField, Model, BooleanField

import settings


db = SqliteDatabase(settings.DATABASE)

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

    email = CharField(index=True, unique=True)
    name = CharField()
    serial = CharField(index=True, unique=True)
    last_sent = DateTimeField(null=True)
    Mon = IntegerField(null=True)
    Tue = IntegerField(null=True)
    Wed = IntegerField(null=True)
    Thu = IntegerField(null=True)
    Fri = IntegerField(null=True)
    Sat = IntegerField(null=True)
    Sun = IntegerField(null=True)
    is_admin = BooleanField(default=False, null=True)
    created = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)

    def is_due(self, date):
        '''
        Determines if a user is due to recieve a digest email
        A user is due if they have a subscription for the current day
        that is between their last_sent datetime and the current datetime
        '''
        zero_minutes = {'minute': 0, 'second': 0, 'microsecond': 0}
        subscription_hour = getattr(self, date.strftime("%a"), None)
        last_sent = self.last_sent or datetime.fromtimestamp(0)

        if not subscription_hour:
            return

        subscription = date.replace(hour=subscription_hour, **zero_minutes)
        return date >= subscription and last_sent < subscription

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
