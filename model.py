from datetime import datetime

from peewee import SqliteDatabase, CharField, ForeignKeyField, \
    DateTimeField, TextField, IntegerField, Model, BooleanField

import settings


db = SqliteDatabase(settings.DATABASE)


class User(Model):
    class Meta: database = db
    email = CharField(index=True)
    name = CharField()
    last_sent = DateTimeField(null=True)
    Mon = IntegerField(null=True)
    Tue = IntegerField(null=True)
    Wed = IntegerField(null=True)
    Thu = IntegerField(null=True)
    Fri = IntegerField(null=True)
    Sat = IntegerField(null=True)
    Sun = IntegerField(null=True)
    created = DateTimeField(default=datetime.now)
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)

    def is_due(self, date):
        send_hour = getattr(self, date.strftime("%a"))
        last_sent = self.last_sent or self.created
        return all([
            send_hour >= 0,
            send_hour <= date.hour,
            (last_sent.day != date.day or last_sent.hour < send_hour),
            self.name == 'Josh'
        ])


class Task(Model):
    class Meta: database = db
    user = ForeignKeyField(User)
    date = DateTimeField(default=datetime.now)
    description = TextField()
