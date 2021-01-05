import sys

from pyceo import Cli


class Foo(Cli):
    def bar(self):
        """BAR"""
        pass


class Lorem(Cli):
    _intro = (
        "Lorem ipsum is placeholder text commonly used for previewing layouts"
        " and visual mockups."
    )

    def ipsum(self):
        """IPSUM

        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat.
        """
        pass

    def sit(self):
        """SIT"""
        pass


class Manager(Cli):
    _intro = "Hello World!"

    def a(self):
        """AAA"""
        pass

    def b(self):
        """BBB"""
        pass

    foo = Foo
    lorem = Lorem


def test_main_help(get_out_text):
    cli = Manager()
    sys.argv = ["manage.py", "--help"]
    cli()

    assert """
 Hello World!

 Available Commands (run with --help for more information)

   a            AAA
   b            BBB
   foo
     bar          BAR
   lorem
     ipsum        IPSUM
     sit          SIT

""" == get_out_text()


def test_subcommand_help(get_out_text):
    cli = Manager()
    sys.argv = ["manage.py", "lorem"]
    cli()

    assert """
 Lorem ipsum is placeholder text commonly used for previewing layouts and visual mockups.

 Available Commands (run with --help for more information)

   ipsum        IPSUM
   sit          SIT

""" == get_out_text()


def test_command_help(get_out_text):
    cli = Manager()
    sys.argv = ["manage.py", "lorem", "ipsum", "--help"]
    cli()

    assert """
 IPSUM

 Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
 tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
 veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
 commodo consequat.
"""
