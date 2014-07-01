import re
import logging
from itertools import ifilter
from datetime import datetime, timedelta
from calendar import day_abbr as DAYS

from prettytable import PrettyTable

from bottle import SimpleTemplate
import settings
from mailclient import MailClient, Subjects
from model import User, Task

DIRECTIVE = 0
OPERAND = 1
ARGUMENT = 2

class Manager(object):

    date_patterns = [
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

    days_ago = re.compile('^(\d+) days? ago$')

    def __init__(self):
        '''
        Creates an Ansible manager.
        During instantiation the manager will:
            authenticate with the SMTP server
            load templates
        '''

        self.mail_client = MailClient()


    def get_template(self, filename):
        '''
        Loads a template from the specified filename
        filename = The name of the file to load as a template
        '''

        input_file = open(filename)
        data = input_file.read()
        input_file.close()
        return SimpleTemplate(data)

    def _parse_date(self, unparsed):
        '''
        Converts a date string to a datetime object
        Allowed formats are defined in date_patterns
        Additionally, "yesterday" and 'X days ago' are
        allowed.
        '''

        default_year = datetime.strptime('', '').year
        parsed = None
        delta = None

        match = self.days_ago.search(unparsed)
        if match:
            delta = int(match.groups()[0])
        elif unparsed.lower() == 'yesterday':
            delta = 1

        if delta:
            return datetime.now() - timedelta(delta)

        for pattern in self.date_patterns:
            try:
                parsed = datetime.strptime(unparsed, pattern)
                break;
            except ValueError:
                pass

        if parsed and parsed.year == default_year:
            parsed = parsed.replace(year = datetime.now().year)

        return parsed



class CronManager(Manager):

    def __init__(self):
        super(CronManager, self).__init__()
        self.digest_template = self.get_template(settings.Templates.DIGEST_EMAIL)

    def format_tasks(self, tasks):
        '''
        Converts tasks to a nested structure for use in the digest template
        tasks = A Peewee Task query
        '''

        tasks = [task for task in tasks] 
        user = tasks[0].user.name
        date = tasks[0].date.strftime('%d/%m/%Y')

        userlist = []
        userdict = {'user': user, 'dates': []}
        datedict = {'date': date}
        tasklist = []

        for task in tasks:
            taskdate = task.date.strftime("%d/%m/%Y")
            if taskdate != date or task.user.name != user:
                datedict['tasks'] = tasklist
                userdict['dates'].append(datedict)

                date = taskdate
                datedict = {'date': date}
                tasklist = []

            if task.user.name != user:
                userlist.append(userdict)
                user = task.user.name
                userdict = {'user': user, 'dates': []}

            tasklist.append(task)

        datedict['tasks'] = tasklist
        userdict['dates'].append(datedict)
        userlist.append(userdict)
        return userlist

    def get_message_vars(self, user, now):
        '''
        Prepares a dict of variables to use in the digest template
        user = A User from the User table
        now = a datetime object representing the current time
        '''

        last_sent = user.last_sent or user.created
        tasks = Task.select().where((Task.date>last_sent))\
            .order_by(Task.user.name, Task.date)
        tasks = [task for task in tasks]
        print "Found {0} tasks".format(len(tasks))

        return {
            'name': user.name,
            'start': last_sent.strftime("%B %d, %Y"),
            'end': now.strftime("%B %d, %Y"),
            'tasklist': self.format_tasks(tasks),
            'date': now.strftime("%B %d, %Y at %I:%M:%S %p"),
            'sender': settings.SENDER,
        }

    def create_digest(self, users):
        '''
        Creates a digest email for all users if:
            The user is due to recieve a digest
            There are tasks to report
        users = A Peewee User query
        '''

        print "Running cron"
        now = datetime.now()
        for user in ifilter(lambda user: user.is_due(now), users):
            print "Creating digest for {0}".format(user.name)
            try:
                vars = self.get_message_vars(user, now)
                if vars:
                    body = self.digest_template.render(**vars)
                    self.mail_client.send(user, body, Subjects.DIGEST)
                user.update_last_sent(now)
            except Exception as e:
                logging.error("Failed to send email to {0}".format(user.name))
                logging.error(e)


class AdminManager(Manager):

    def __init__(self):
        super(AdminManager, self).__init__()
        self.all_template = self.get_template(settings.Templates.ADMIN)
        self.user_template = self.get_template(settings.Templates.USER)
        self.view_template = self.get_template(settings.Templates.DB_VIEW)

    def create(self, name, email):
        '''
        Adds a user to the user table
        email = the user's email
        name = the user's name
        '''

        try:
            user = User.get(email=email)
            user.name = name
            user.is_active = True
            user.save()
        except User.DoesNotExist:
            User.create(name=name, email=email)
        return "Added user '{0}' with email '{1}'".format(name, email)

    def remove(self, id):
        ''' 
        Marks a user as inactive.
        Inactive users cannot report tasks or receieve emails
        email = the user's email
        '''

        try:
            leaving = User.get(id=id)
            leaving.is_active = False
            leaving.save()
            message = "Removed user '{0}' with email '{1}'".format(leaving.name, leaving.email)
        except (User.DoesNotExist, ValueError):
            message = "No user with id '{0}'".format(id)
        return message

    def update(self, id, schedule):
        try:
            user = User.get(id=id)
        except (User.DoesNotExist, ValueError):
            return
        for day in DAYS:
            time = schedule.get(day)
            try:
                time = int(time)
                if time < 0 or time >= 24:
                    time = None
            except:
                time = None
            setattr(user, day, time)
        user.save()

    def get_user_table(self):
        table = PrettyTable(["Email", "Name", "Last sent", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "created", "active"])
        for user in User.select():
            table.add_row([
                user.email,
                user.name,
                user.last_sent,
                user.Mon,
                user.Tue,
                user.Wed,
                user.Thu,
                user.Fri,
                user.Sat,
                user.Sun,
                user.created,
                user.is_active,
            ])
        return table

    def get_task_table(self, start = None, end = None):
        table = PrettyTable(["Name", 'Date', 'Description'])
        start = self._parse_date(start)
        end = self._parse_date(end)
        query = Task.select().where(Task.date.between(start, end)) if\
            all([start, end]) else Task.select()

        for task in query:
            table.add_row([task.user.name, task.date, task.description])

        return table


class ServerManager(Manager):

    def __init__(self):
        super(ServerManager, self).__init__()
        self.help_template = self.get_template(settings.Templates.HELP_EMAIL)
        self.response_template = self.get_template(settings.Templates.RESPONSE_EMAIL)
        self.subscription_template = self.get_template(settings.Templates.SUBSCRIPTIONS)

    def add_task(self, user, body, date_unparsed = None):
        '''
        Add a task.
        user = A user object from the User table
        body = The body of an incoming email.
            Each line will be made into a new task
        '''

        details = {'user': user}
        date_parsed = self._parse_date(date_unparsed.strip())

        if date_parsed:
            details['date'] = date_parsed

        for task in body.split('\n'):
            details['description'] = task
            Task.create(**details)

    def manage(self, user, body):
        '''
        Executes manage commands
        user = A User object from the User table
        body = the body of an incoming email.
            Each line will be interpreted as a separate command
        '''

        responses = []
        for command in map(lambda x: x.split(), body.split('\n')):
            if not len(command):
                continue

            directive = command[DIRECTIVE].lower()

            # Is the command recognized
            if directive not in ['set', 'remove']:
                responses.append("Unrecognized command: {0}".format(' '.join(command)))
                continue

            # Does the command have the proper number of arguments
            if (directive in ['set'] and len(command) < 3 )\
            or (directive in ['remove'] and len(command) < 2):
                responses.append("Missing argument: {0}".format(' '.join(command)))
                continue

            day = command[OPERAND][:3].capitalize()

            # Is the day valid
            if (not hasattr(user, day)):
                responses.append("Invalid day: {0}".format(' '.join(command)))
                continue

            # Is the hour a number. Not necessary for remove
            try:
                hour = int(command[ARGUMENT]) if directive == 'set' else None
            except:
                responses.append("Invalid time: {0}".format(' '.join(command)))
                continue

            # Is the hour either None (for remove) or between 0 and 23 (for set)
            if not hour is None and any([hour < 0, hour > 23]):
                responses.append("Invalid arguments: {0}".format(' '.join(command)))
                continue

            # Make the modification & add the appropriate response
            setattr(user, day, hour)
            response = 'We will email you at {0}:00 on {1}.'.format(hour, day) if hour\
                else 'We will no longer email you on {0}.'.format(day)
            responses.append(response)

        user.save()
        body = self.response_template.render(responses=responses, user=user, sender=settings.SENDER)
        self.mail_client.send(user, body, Subjects.RESPONSE)
        return body

    def show_subscriptions(self, user):
        body = self.subscription_template.render(user=user, sender=settings.SENDER)
        self.mail_client.send(user, body, Subjects.SUBSCRIPTIONS)
        return body

    def help(self, user):
        '''
        Sends a help email to the specified user
        user = A User object from the User table
        '''

        body = self.help_template.render(user=user)
        self.mail_client.send(user, body, Subjects.HELP)
        return body
