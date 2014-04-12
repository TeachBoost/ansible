import logging

from model import User
from manager import Manager

# Cron for creating digest emails
if __name__ == '__main__':
    try:
        manager = Manager()
        manager.create_digest(User.select())
    except Exception as e:
        logging.error(e)
