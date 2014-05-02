import logging
from os import path

import credentials

''' The following values will need to be configured to work with the local system '''

PUBLIC_URL = 'ansible'

# Details about the smtp server
SMTP = {
    'host': 'smtp.mailgun.org',
    'port': 587,
}

# Enable debugging
DEBUG = True
# Enable email sending
SEND_EMAIL = False

# Details about the Bottle server which listens for incomming messages
# Only used when running from terminal. Configure nginx server separately.
SERVER = {
    #'server': 'python_server',
    'host': 'localhost', 
    'port': 8080,
    'debug': DEBUG, # In debug mode, error messages will be returned in HTTP responses
}

# The name of the database file
DATABASE = 'ansible.db'


''' The rest of the values don't need to be modified, but still can be... '''

SENDER = credentials.SENDER
PASSWORD = credentials.PASSWORD
KEY = credentials.KEY

# The location of templates
TEMPLATE_DIR = 'templates/'

# Individual templates
class Templates:
    TEST_FORM = path.join(TEMPLATE_DIR, 'test_form')
    DIGEST_EMAIL = path.join(TEMPLATE_DIR, 'digest_email')
    HELP_EMAIL = path.join(TEMPLATE_DIR, 'help_email')
    RESPONSE_EMAIL = path.join(TEMPLATE_DIR, 'response_email')

# Logging setup
logging.basicConfig(
    filename="log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s"
)