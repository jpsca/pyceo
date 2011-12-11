#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pyceo import Manager


manager = Manager()

@manager.command
def runserver(host='0.0.0.0', port=None, **kwargs):
    """[-host HOST] [-port PORT]
    Runs the application on the local development server.
    """
    print 'runserver ( host=', host, 'port=', port, 'kwargs=', kwargs, ')'


@manager.command
def initdb():
    """Create the database tables (if they don't exist)"""
    print 'initdb'


@manager.command
def change_password(login, passw):
    """[-login] LOGIN [-passw] NEW_PASSWORD
    Changes the password of an existing user."""
    print 'change_password ( login=', login, 'passw=', passw, ')'


if __name__ == "__main__":
    manager.run(default='runserver')
