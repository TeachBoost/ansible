#! /usr/bin/python

''' Initalization script. Should only be run once. '''

import os
import sys
from datetime import timedelta

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
    User.create(name="Jason", email="jason@teachboost.com")
    User.create(name="Mike", email="mike@teachboost.com", is_admin=True)
    User.create(name="Andrew", email="andrew@teachboost.com")
    User.create(name="Peter", email="peter@teachboost.com")
    User.create(name="Jill", email="jill@teachboost.com")
    User.create(name="Kate", email="kate@teachboost.com")
    User.create(name="Josh", email="josh@teachboost.com", is_admin=True)
    User.create(name="Ben", email="ben@teachboost.com")
    User.create(name="Andy", email="amacdonald@teachboost.com")
    User.create(name="Amy", email="amy@teachboost.com")
    User.create(name="Talia", email="talia@teachboost.com")

if __name__ == "__main__":
    force = '-f' in sys.argv
    exists = delete_db(settings.DATABASE, force)
    if exists:
        print "A database already exists. Run with -f to delete and reinitialize"
    else:
        create_tables()
        populate()
