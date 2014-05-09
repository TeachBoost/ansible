import logging
from os import path
from deploy import config

# The base url of the site
PUBLIC_URL = config.PUBLIC_URL

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
    SERVER['debug'] = DEBUG # In debug mode, error messages will be returned in HTTP responses

# The name of the database file
DATABASE = config.DATABASE

# The email addres messages will come from
SENDER = config.SENDER

# Password for sending emails from specified smtp server
PASSWORD = config.PASSWORD

# Key all incomming email requests must be signed with
KEY = config.KEY

# The location of templates
TEMPLATE_DIR = 'templates/'

# Individual templates
class Templates:
    TEST_FORM = path.join(TEMPLATE_DIR, 'test_form')
    DIGEST_EMAIL = path.join(TEMPLATE_DIR, 'digest_email')
    HELP_EMAIL = path.join(TEMPLATE_DIR, 'help_email')
    RESPONSE_EMAIL = path.join(TEMPLATE_DIR, 'response_email')
    ADMIN = path.join(TEMPLATE_DIR, 'admin')
    USER = path.join(TEMPLATE_DIR, 'user')

# Logging setup
logging.basicConfig(
    filename="log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s"
)