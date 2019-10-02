from pyceo import Manager, param, option


cli = Manager("Welcome to Proper v1.2.3")


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


@cli.command(group="db")
@option("message", help="Revision message")
@option("sql", help="Dont emit SQL to database - dump to standard output instead")
@option("head", help="Specify head or <branchname>@head to base new revision on")
def migrate(**kwargs):
    """Autogenerate a new revision file.

    This is an alias for "revision --autogenerate"."""
    pass


@cli.command(group="db")
@option("name", help="Name of section in .ini file to use for Alembic config")
def branches(**kwargs):
    """Show current branch points.
    """
    pass


if __name__ == "__main__":
    # cli.run(default="new")
    cli.run()
