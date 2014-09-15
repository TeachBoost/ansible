import re
from datetime import datetime, timedelta
from itertools import takewhile, ifilter
import logging

from bottle import request, HTTPResponse

from model import Task
from library.auth import debug_only, auth_email
from library.template import Template
from library.mailclient import MailClient, Subjects
import settings

template = Template()
mailclient = MailClient()

HELP_REGEX = re.compile('help')
MANAGE_REGEX = re.compile('manage')
SUBSCRIPTION_REGEX = re.compile('subscriptions')
DAYS_AGO = re.compile('^(\d+) days? ago$')
DATE_PATTERNS = [
    '%m/%d',
    '%m-%d',
    '%B %d',
    '%b %d',
    '%m/%d/%y',
    '%m/%d/%Y',
    '%m-%d-%y',
    '%m-%d-%Y',
    '%B %d %Y',
    '%B %d %y',
    '%B %d, %Y',
    '%B %d, %y',
    '%b %d %y',
    '%b %d %Y',
    '%b %d, %y',
    '%b %d, %Y',
]


@debug_only
def test_form():
    return template.render('test_form.tpl', key=settings.KEY)


@auth_email
def receive_email(user):
    subject = request.forms.get('Subject')
    body = request.forms.get('stripped-text')

    if HELP_REGEX.search(subject):
        body = help(user)
        email = mailclient.send(user, body, Subjects.HELP) if body else None

    elif SUBSCRIPTION_REGEX.search(subject):
        body = read_subscriptions(user)
        email = mailclient.send(user, body, Subjects.SUBSCRIPTIONS)\
            if body else None

#     elif MANAGE_REGEX.search(subject):
#         body = update_subscriptions(user, body)

    else:
        body = log_tasks(user, subject, body)
        email = True

    if not email:
        return HTTPResponse(500)

    if settings.DEBUG:
        return template.render(
            'show_email.tpl',
            email=(email if email is not True else ["No response"]), user=user
        )
    else:
        return HTTPResponse(status=200)


def parse_date(unparsed):
    '''
    Converts a date string to a datetime object
    Allowed formats are defined in date_patterns
    Additionally, "yesterday" and 'X days ago' are
    allowed.
    '''
    default_year = datetime.strptime('', '').year
    parsed = None
    delta = None

    match = DAYS_AGO.search(unparsed)
    if match:
        delta = int(match.groups()[0])
    elif unparsed.lower() == 'yesterday':
        delta = 1

    if delta:
        return datetime.now() - timedelta(delta)

    for pattern in DATE_PATTERNS:
        try:
            parsed = datetime.strptime(unparsed, pattern)
            break
        except ValueError:
            pass

    if parsed and parsed.year == default_year:
        parsed = parsed.replace(year=datetime.now().year)

    return parsed


def help(user):
    return template.render('email_help.tpl', user=user)


def read_subscriptions(user):
    return template.render(
        'email_subscriptions.tpl', user=user, sender=settings.SENDER)


# def update_subscriptions(user, body):
#     pass


def log_tasks(user, subject, body):
    details = {'user': user}
    date = parse_date(subject)
    if date:
        details['date'] = date - timedelta(hours=user.timezone)

    for task in parse_body(body):
        details['description'] = task
        Task.create(**details)


def is_not_signature(line):
    return not reduce(
        lambda accum, pattern: accum or re.search(pattern, line),
        [
            '^-- ?\n',
            '-----Original Message-----',
            '________________________________',
            '^On.*wrote:\n',
            '^From: ',
            '^Sent from my iPhone',
            '^Sent from my BlackBerry',
        ],
        False
    )


def parse_body(body):
    lines = re.sub('\n(?!\n)', ' ', re.sub('\r', '', body)).split('\n')
    return ifilter(None, takewhile(is_not_signature, map(str.strip, lines)))
