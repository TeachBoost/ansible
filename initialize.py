#! /usr/bin/python
''' Initalization script. Should only be run once. '''

import os
import sys

from model import User, Task
import settings

tables = {'user': User, 'task': Task}

users = [
    {
        'name': "Jason",
        'email': "jason@teachboost.com",
        'serial': '08',
    },
    {
        'name':  'Mike',
        'email': 'mike@teachboost.com',
        'serial': '02',
        'is_admin': True,
    },
    {
        'name':  'Andrew',
        'email': 'andrew@teachboost.com',
        'serial': '03',
    },
    {
        'name':  'Peter',
        'email': 'peter@teachboost.com',
        'serial': '09',
    },
    {
        'name':  'Jill',
        'email': 'jill@teachboost.com',
        'serial': '0A',
    },
    {
        'name':  'Kate',
        'email': 'kate@teachboost.com',
        'serial': '0C',
    },
    {
        'name':  'Josh',
        'email': 'josh@teachboost.com',
        'serial': '06',
        'is_admin': True,
    },
    {
        'name':  'Ben',
        'email': 'ben@teachboost.com',
        'serial': '0B',
    },
    {
        'name':  'Andy',
        'email': 'amacdonald@teachboost.com',
        'serial': '0E',
    },
    {
        'name':  'Amy',
        'email': 'amy@teachboost.com',
        'serial': '0D',
    },
    {
        'name':  'Talia',
        'email': 'talia@teachboost.com',
        'serial': '07',
    },
]


def create_tables():
    User.create_table()
    Task.create_table()


def populate():
    for user in users:
        User.create(Mon=22, Thu=22, **user)


def rebuild_table(table):
    Table = tables[table]
    Table.drop_table()
    Table.create_table()
    if Table == User:
        populate()


def initialize(delete, table):
    if table:
        rebuild_table(table)
    else:
        if delete:
            os.remove(settings.DATABASE)
        create_tables()
        populate()


if __name__ == "__main__":
    table_index = sys.argv.index('-t') if '-t' in sys.argv else None
    table = sys.argv[table_index + 1] if table_index is not None else None
    delete = '-d' in sys.argv
    exists = os.path.isfile(settings.DATABASE)

    if exists and not (delete or table):
        print ''''A database already exists.
        Run with -d to delete existing database
        Run with -t <tablename> to rebuild a single table'''
    else:
        initialize(exists and delete, table)
