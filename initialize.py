''' Initalization script. Should only be run once. '''

import os
from datetime import datetime

from model import User, Task
import settings


DEFAULT_TIMES = {
    'Mon': 9,
    'Thu': 10,
    'Fri': 8,
}

def delete_db(db_file):
    os.remove(db_file)

def create_tables():
    User.create_table()
    Task.create_table()

def populate():
    User.create(name="Andrew", email="andrew@teachboost.com", **DEFAULT_TIMES)
    User.create(name="Jason", email="jason@teachboost.com", **DEFAULT_TIMES)
    User.create(name="Jill", email="jill@teachboost.com", **DEFAULT_TIMES)
    User.create(name="Josh", email="josh@teachboost.com", **DEFAULT_TIMES)
    User.create(name="Kate", email="kate@teachboost.com", **DEFAULT_TIMES)
    User.create(name="Mike", email="mike@teachboost.com", **DEFAULT_TIMES)
    User.create(name="Peter", email="peter@teachboost.com", **DEFAULT_TIMES)


if __name__ == "__main__":
    delete_db(settings.DATABASE)
    create_tables()
    populate()
