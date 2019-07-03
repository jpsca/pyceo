import sys

import pyceo


def test_intro_in_help(capsys):
    intro = "This is my intro"
    cli = pyceo.Manager(intro)

    sys.argv = ["manage.py", "help"]
    cli.run()

    captured = capsys.readouterr()
    assert intro in captured.out


def test_error_wrong_args(capsys):
    cli = pyceo.Manager()

    @cli.command
    def hello():
        pass

    sys.argv = ["manage.py", "hello", "world"]
    cli.run()

    captured = capsys.readouterr()
    assert "ERROR" in captured.out
