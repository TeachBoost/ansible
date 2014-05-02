#! /usr/bin/python

import logging

import settings
from model import User
from manager import CronManager

# Cron for creating digest emails
if __name__ == '__main__':
    try:
        manager = CronManager()
        manager.create_digest(User.select())
    except Exception as e:
        logging.error(e)
        if settings.DEBUG:
            raise
