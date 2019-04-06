=========
pyCEO
=========

A minimal and composable command-line toolkit **focused on looking good and delegate all the real work**.

.. code:: python

    from pyceo import Manager

    manager = Manager()

    @manager.command
    def runserver(host='0.0.0.0', port=None, **kwargs):
        """[-host HOST] [-port PORT]
        Runs the application on the local development server.
        """
        app.run(host, port, **kwargs)


    @manager.command
    def initdb():
        """Create the database tables (if they don't exist)"""
        from app.models import db

        db.create_all()


    @manager.command
    def change_password(login, passw):
        """[-login] LOGIN [-passw] NEW_PASSWORD
        Changes the password of an existing user."""
        from app.app import auth

        auth.change_password(login, passw)


    if __name__ == "__main__":
        manager.run(default='runserver')


Go to the examples/ folder and run::

    python manage.py help

to see the result.


Why don't just use optparse or argparse?
-----------------------------------------

Because this looks better and is easier to use and understand.

Why don't just use click?
-----------------------------------------

Because this looks better and is easier to use and understand.


:license: MIT, see LICENSE for more details.
