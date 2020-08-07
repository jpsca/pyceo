import sys

import pytest

from pyceo import Manager, param, option


def test_intro_in_help(capsys):
    intro = "This is my intro"
    cli = Manager(intro)

    sys.argv = ["manage.py", "help"]
    cli.run()

    captured = capsys.readouterr()
    print(captured.out)
    assert intro in captured.out


def test_error_too_many_args(capsys):
    cli = Manager(catch_errors=True)

    @cli.command()
    def hello():
        pass

    sys.argv = ["manage.py", "hello", "world"]
    cli.run()

    captured = capsys.readouterr()
    print(captured.out)
    assert "hello() takes 0 positional arguments but 1 was given" in captured.out


def test_error_missing_args(capsys):
    cli = Manager(catch_errors=True)

    @cli.command()
    @param("path")
    def hello(path):
        pass

    sys.argv = ["manage.py", "hello"]
    cli.run()

    captured = capsys.readouterr()
    print(captured.out)
    assert "hello() missing 1 required positional argument" in captured.out


def test_missing_args_with_defaults_is_not_an_error(capsys):
    cli = Manager()

    @cli.command()
    @param("path")
    def hello(path="/"):
        pass

    sys.argv = ["manage.py", "hello"]
    cli.run()

    captured = capsys.readouterr()
    print(captured.out)
    assert "ERROR" not in captured.out


def test_error_wrong_option_type(capsys):
    cli = Manager()

    @cli.command()
    @option("port", type=int)
    def hello(port=1):
        pass

    sys.argv = ["manage.py", "hello", "--port", "world"]
    cli.run()

    captured = capsys.readouterr()
    print(captured.out)
    assert "Wrong argument for `port`" in captured.out


def test_type_option(capsys):
    cli = Manager()

    @cli.command()
    @option("port", type=int)
    def hello(port=1):
        print(f"Port is {type(port)}")

    sys.argv = ["manage.py", "hello", "--port", "123"]
    cli.run()

    captured = capsys.readouterr()
    print(captured.out)
    assert "Port is <class 'int'>" in captured.out
    assert "Port is <class 'str'>" not in captured.out


def test_group_in_name(capsys):
    cli = Manager()
    msg = "Hello world!"

    @cli.command(name="foo:bar")
    def hello():
        print(msg)

    sys.argv = ["manage.py", "foo:bar"]
    cli.run()

    captured = capsys.readouterr()
    print(captured.out)
    assert msg in captured.out


def test_name_and_group_as_arg(capsys):
    cli = Manager()
    msg = "Hello world!"

    @cli.command(group="foo", name="bar")
    def hello():
        print(msg)

    sys.argv = ["manage.py", "foo:bar"]
    cli.run()

    captured = capsys.readouterr()
    print(captured.out)
    assert msg in captured.out


def test_no_repeated_names(capsys):
    cli = Manager()

    @cli.command(name="qwertyuiop", help="WRONG")
    def a():
        return "a"

    @cli.command(name="qwertyuiop", help="RIGHT")
    def b():
        return "b"

    sys.argv = ["manage.py", "help"]
    cli.run()

    captured = capsys.readouterr()
    print(captured.out)
    assert "qwertyuiop" in captured.out
    assert "RIGHT" in captured.out
    assert "WRONG" not in captured.out


def test_merge(get_out_text):
    cli = Manager()
    cli2 = Manager()

    @cli.command(help="AAA")
    def a():
        pass

    @cli2.command(help="BBB")
    def b():
        pass

    cli.merge(cli2)
    sys.argv = ["manage.py", "help"]
    cli.run()

    assert """

 Usage
   manage <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

   All commands can be run with -h (or --help) for more information.

 Available Commands
   a            AAA
   b            BBB

""" == get_out_text()


def test_merge_groups(get_out_text):
    cli = Manager()
    cli2 = Manager()

    @cli.command(help="AAA", name="foo:a")
    def a():
        pass

    @cli2.command(help="BBB", name="bar:b")
    def b():
        pass

    cli.merge(cli2)
    sys.argv = ["manage.py", "help"]
    cli.run()

    assert """

 Usage
   manage <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

   All commands can be run with -h (or --help) for more information.

 Available Commands

  foo
   foo:a        AAA

  bar
   bar:b        BBB

""" == get_out_text()


def test_merge_same_group(get_out_text):
    cli = Manager()
    cli2 = Manager()

    @cli.command(help="AAA", name="foo:a")
    def a():
        pass

    @cli2.command(help="BBB", name="foo:b")
    def b():
        pass

    cli.merge(cli2)
    sys.argv = ["manage.py", "help"]
    cli.run()

    assert """

 Usage
   manage <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

   All commands can be run with -h (or --help) for more information.

 Available Commands

  foo
   foo:a        AAA
   foo:b        BBB

""" == get_out_text()


def test_merge_to_group():
    cli = Manager()
    cli2 = Manager()

    @cli.command(help="AAA", name="foo:a")
    def a():
        pass

    @cli2.command(help="BBB")
    def b():
        pass

    cli.merge(cli2, group="foo")
    sys.argv = ["manage.py", "help"]
    cli.run()

#     assert """

#  Usage
#    manage <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

#    All commands can be run with -h (or --help) for more information.

#  Available Commands

#   foo
#    foo:a        AAA
#    foo:b        BBB

# """ == get_out_text()


def test_merge_explicit_groups(get_out_text):
    cli = Manager()
    cli2 = Manager()

    @cli.command(help="AAA", name="a", group="foo")
    def a():
        pass

    @cli2.command(help="BBB", name="b", group="bar")
    def b():
        pass

    cli.merge(cli2)
    sys.argv = ["manage.py", "help"]
    cli.run()

    assert """

 Usage
   manage <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

   All commands can be run with -h (or --help) for more information.

 Available Commands

  foo
   foo:a        AAA

  bar
   bar:b        BBB

""" == get_out_text()


def test_add_command(get_out_text):
    cli = Manager()

    def a():
        """AAA"""

    def b():
        """BBB"""

    cli.add_commands([a, b])
    sys.argv = ["manage.py", "help"]
    cli.run()

    assert """

 Usage
   manage <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

   All commands can be run with -h (or --help) for more information.

 Available Commands
   a            AAA
   b            BBB

""" == get_out_text()


def test_add_command_to_group(get_out_text):
    cli = Manager()

    def a():
        """AAA"""

    def b():
        """BBB"""

    cli.add_commands([a, b], group="foo")
    sys.argv = ["manage.py", "help"]
    cli.run()

    assert """

 Usage
   manage <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

   All commands can be run with -h (or --help) for more information.

 Available Commands

  foo
   foo:a        AAA
   foo:b        BBB

""" == get_out_text()


def test_add_command_with_data(get_out_text):
    cli = Manager()

    def a():
        pass

    cli.add_command(a, help="AAA", name="bar", group="foo")
    sys.argv = ["manage.py", "help"]
    cli.run()

    assert """

 Usage
   manage <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

   All commands can be run with -h (or --help) for more information.

 Available Commands

  foo
   foo:bar      AAA

""" == get_out_text()
