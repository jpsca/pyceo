import re
import sys

from pyceo import Manager, param, option


cli = Manager("Welcome")


@cli.command(help="Creates a new Proper application at `path`.")
@param("path", help="Where to create the new application.")
@option("quiet", help="Supress all output.")
def new(path):
    """The `proper new` command creates a new Proper application with a default
    directory structure and configuration at the path you specify.

    Example: `proper new ~/Code/blog`
    This generates a skeletal Proper application at `~/Code/blog`.
    """
    pass


@cli.command()
@option("num", type=int)  # Optional type
def fizzbuzz(num=3):
    """A bad fizz buzz."""
    print("fizz " * num + "buzz")

cli2 = Manager()


@cli2.command(group="db")
@option("message", help="Revision message")
@option("sql", help="Dont emit SQL to database - dump to standard output instead")
@option("head", help="Specify head or <branchname>@head to base new revision on")
def migrate(**kwargs):
    """Autogenerate a new revision file.

    This is an alias for "revision --autogenerate"."""
    pass


@cli2.command(group="db")
@option("name", help="Name of section in .ini file to use for Alembic config")
def branches(**kwargs):
    """Show current branch points.
    """
    pass


@cli2.command(group="auth")
def users():
    pass


@cli2.command(group="auth")
@param("login")
@param("passw")
def add_user(login, passw):
    pass

cli.merge(cli2)


EXPECTED = """ Welcome

 Usage
   test_full <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

   All commands can be run with -h (or --help) for more information.

 Available Commands
   new          Creates a new Proper application at `path`.
   fizzbuzz     A bad fizz buzz.

  db
   db:migrate   Autogenerate a new revision file.
   db:branches  Show current branch points.

  auth
   auth:users
   auth:add_user

"""

NON_VISIBLE = [
    "\x1b[0m",
    "\x1b[1m",
    "\x1b[33m",
    "\x1b[36m",
    "\x1b[39m",
    "\x1b[92m",
]


def test_full(capsys):
    sys.argv = ["test_full.py", "help"]
    cli.run()
    out = capsys.readouterr().out
    out = strip_non_visible(out)
    print(out)
    assert out == EXPECTED


def strip_non_visible(text):
    for nv in NON_VISIBLE:
        text = text.replace(nv, "")
    text = re.sub(r"[ ]+\n", r"\n", text)
    return text

if __name__ == "__main__":
    cli.run()
