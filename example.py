# example.py
from pyceo import Cli


class DBCli(Cli):
    _intro = "Database-related commands"

    def migrate(self, message):
        """Autogenerate a new revision file.

        This is an alias for "revision --autogenerate".

        Arguments:

        - message: Revision message

        """
        pass

    def branches(self):
        """Show all branches."""
        pass


class MyCli(Cli):
    _intro = "Welcome to PyCeo 3"

    def new(self, path, quiet=False):
        """Creates a new Proper application at `path`.

        Arguments:

        - path: Where to create the new application.
        - quiet [False]: Supress all output.
        """
        pass

    def hello(count, name):
        """Simple program that greets NAME for a total of COUNT times."""
        pass

    # A subcommand!
    db = DBCli


cli = MyCli()

if __name__ == "__main__":
    cli()
