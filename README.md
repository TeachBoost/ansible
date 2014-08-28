# Ansible

Team tracking service. Team members send an email with what they've
gotten done for the day, and other team members can subscribe to
receive notifications.

## Dependencies

Install the python dependencies:

    aptitude install uwsgi uwsgi-plugin-python python-bottle nginx
    aptitude install python-pip
    pip install peewee

## Installation

* Run `./ininitalize.py` to set up the database and other requirements.
* Create a `secret.ini` file in `/deploy` for any secret variables that
  should be copied in to your config file.
* Run `'./deploy/install.sh <profile> where <profile> is the name of the
  profile in the `/deploy/env/` directory. Any secret variables will be
  copied into this file. Use the `##VARIABLENAME## key in the environment
  file and set add `VARIABLENAME="value"` lines in the secret.ini file
  to replace with.


