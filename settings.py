import logging
from os import path

from deploy import config

# The base url of the site
BASEPATH = config.BASEPATH  # '/ansible'
# The public path
PUBLIC_URL = config.PUBLIC_URL  # 'localhost:8080'

# The email listener url
EMAIL_PATH = BASEPATH + '/email'
ADMIN_PATH = BASEPATH + '/admin'
STATIC_PATH = BASEPATH + '/static'

# The location of the project's root folder
PROJECT_ROOT = path.dirname(path.abspath(__file__))

# Details about the smtp server
SMTP = {
    'host': config.SMTP_HOST,
    'port': config.SMTP_PORT
}

# Enable debugging
DEBUG = config.DEBUG

# Enable email sending
SEND_EMAIL = config.SEND_EMAIL

# Details about the Bottle server which listens for incomming messages
# Only used when running from terminal. Configure nginx server separately.
SERVER = {}

if hasattr(config, 'SERVER_HOST') and hasattr(config, 'SERVER_PORT'):
    SERVER['host'] = config.SERVER_HOST
    SERVER['port'] = config.SERVER_PORT
    # In debug mode, error messages will be returned in HTTP responses
    SERVER['debug'] = DEBUG

# The name of the database file
DATABASE = config.DATABASE

# The email addres messages will come from
SENDER = config.SENDER

# Password for sending emails from specified smtp server
PASSWORD = config.PASSWORD

# Key all incomming email requests must be signed with
KEY = config.KEY

# The location of templates
TEMPLATE_DIR = path.join(PROJECT_ROOT, 'view/')

# Logging setup
logging.basicConfig(
    filename="log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s"
)
