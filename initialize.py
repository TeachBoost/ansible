#! /usr/bin/python

''' Initalization script. Should only be run once. '''

import os
import sys

from model import User, Task
import settings


def delete_db(db_file, force):
    if os.path.isfile(db_file):
        if force:
            os.remove(db_file)
        else:
            return True


def create_tables():
    User.create_table()
    Task.create_table()


def populate():
    User.create(serial='08', name="Jason", email="jason@teachboost.com")
    User.create(serial='02', name="Mike", email="mike@teachboost.com", is_admin=True)
    User.create(serial='03', name="Andrew", email="andrew@teachboost.com")
    User.create(serial='09', name="Peter", email="peter@teachboost.com")
    User.create(serial='0A', name="Jill", email="jill@teachboost.com")
    User.create(serial='0C', name="Kate", email="kate@teachboost.com")
    User.create(serial='06', name="Josh", email="josh@teachboost.com", is_admin=True)
    User.create(serial='0B', name="Ben", email="ben@teachboost.com")
    User.create(serial='0E', name="Andy", email="amacdonald@teachboost.com")
    User.create(serial='0D', name="Amy", email="amy@teachboost.com")
    User.create(serial='07', name="Talia", email="talia@teachboost.com")

if __name__ == "__main__":
    force = '-f' in sys.argv
    exists = delete_db(settings.DATABASE, force)
    if exists:
        print ''''A database already exists.
        Run with -f to delete and reinitialize'''
    else:
        create_tables()
        populate()
