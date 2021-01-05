from pyceo import Cli


class Assets(Cli):
    def build(self):
        print("You invoked the `assets build` command")

class DB(Cli):
    _intro = "Database-related commands"

    def migrate(self, **kwargs):
        """Autogenerate a new revision file.

        This is an alias for "revision --autogenerate".

        Arguments:

        - message:
            Revision message
        """
        print("You invoked the `db migrate` command")


class MyCli(Cli):
    _intro = "Welcome to PyCeo 3."

    def new(self, path, quiet=False):
        """Creates a new Proper application at `path`.

        The `proper new` command creates a new Proper application with a default
        directory structure and configuration at the path you specify.

        Example: `proper new ~/Code/blog`
        This generates a skeletal Proper application at `~/Code/blog`.

        Arguments:

        - path:
            Where to create the new application.
        - quiet [False]:
            Supress all output.
        """
        print("You invoked the `new` command")

    def a(self):
        """Whatever"""
        print("You invoked the `a` command")

    # Subcommands
    assets = Assets
    db = DB


cli = MyCli()

if __name__ == "__main__":
    cli()
