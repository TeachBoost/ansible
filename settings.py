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
SEND_EMAIL = False

# Deadline time for daily reporting in 24hr UTC time
REPORT_DUE = 21

# Details about the Bottle server which listens for incomming messages
# Only used when running from terminal. Configure nginx server separately.
SERVER = {}

if hasattr(config, 'SERVER_HOST') and hasattr(config, 'SERVER_PORT'):
    SERVER['host'] = config.SERVER_HOST
    SERVER['port'] = config.SERVER_PORT
    # In debug mode, error messages will be returned in HTTP responses
    SERVER['debug'] = DEBUG

# The name of the database file
DATABASE = path.join(PROJECT_ROOT, config.DATABASE)

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
    filename=path.join(PROJECT_ROOT, "log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s"
)

TIMEZONES = [
    (-12, "(GMT -12:00) Eniwetok, Kwajalein"),
    (-11, "(GMT -11:00) Midway Island, Samoa"),
    (-10, "(GMT -10:00) Hawaii"),
    (-9, "(GMT -9:00) Alaska"),
    (-8, "(GMT -8:00) Pacific Time (US & Canada)"),
    (-7, "(GMT -7:00) Mountain Time (US & Canada)"),
    (-6, "(GMT -6:00) Central Time (US & Canada), Mexico City"),
    (-5, "(GMT -5:00) Eastern Time (US & Canada), Bogota, Lima"),
    (-4, "(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz"),
    (-3.5, "(GMT -3:30) Newfoundland"),
    (-3, "(GMT -3:00) Brazil, Buenos Aires, Georgetown"),
    (-2, "(GMT -2:00) Mid-Atlantic"),
    (-1, "(GMT -1:00 hour) Azores, Cape Verde Islands"),
    (0, "(GMT) Western Europe Time, London, Lisbon, Casablanca"),
    (1, "(GMT +1:00 hour) Brussels, Copenhagen, Madrid, Paris"),
    (2, "(GMT +2:00) Kaliningrad, South Africa"),
    (3, "(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg"),
    (3.5, "(GMT +3:30) Tehran"),
    (4, "(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi"),
    (4.5, "(GMT +4:30) Kabul"),
    (5, "(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent"),
    (5.5, "(GMT +5:30) Bombay, Calcutta, Madras, New Delhi"),
    (5.75, "(GMT +5:45) Kathmandu"),
    (6, "(GMT +6:00) Almaty, Dhaka, Colombo"),
    (7, "(GMT +7:00) Bangkok, Hanoi, Jakarta"),
    (8, "(GMT +8:00) Beijing, Perth, Singapore, Hong Kong"),
    (9, "(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk"),
    (9.5, "(GMT +9:30) Adelaide, Darwin"),
    (10, "(GMT +10:00) Eastern Australia, Guam, Vladivostok"),
    (11, "(GMT +11:00) Magadan, Solomon Islands, New Caledonia"),
    (12, "(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka"),
]
