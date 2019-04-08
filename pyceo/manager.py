"""
# pyceo.main

Create management scripts for your applications so you can do
things like `python manage.py runserver`.

"""
import sys
import textwrap

from .command import Command, HELP_COMMANDS
from .parser import parse_args


__all__ = ("Manager", "manager")


class Manager(object):

    parent = ""

    def __init__(self, func, help="", name=None):
        self.func = func
        self.name = name or func.__name__
        self.description = textwrap.dedent(func.__doc__ or "")
        self.help = help

        self.managers = {}
        self.commands = {}

    def __call__(self, *args, **opts):
        return self.func(*args, **opts)

    def run(self, default=None, sys_args=None, parent=None):
        """Parse the command line arguments.

        default:
            Name of default command to run if no arguments are passed.

        """
        self.parent = parent
        if sys_args is None:
            sys_args = sys.argv
            self.parent, *sys_args = sys_args

        name = default
        if sys_args:
            name, *sys_args = sys_args

        if name is None or name.lstrip("-") in HELP_COMMANDS:
            self.show_help()
            return

        sub_manager = self.managers.get(name)
        if sub_manager:
            sub_parent = "{} {}".format(self.parent, self.name)
            return sub_manager.run(sys_args=sys_args, parent=sub_parent)

        command = self.commands.get(name)
        if command is None:
            self.show_error("{} command not found".format(name))
            self.show_help()
            return

        args, opts = parse_args(sys_args)
        return command.run(*args, **opts)

    def show_error(self, msg):
        print("\nERROR:", msg)

    def show_help(self):
        print("\nHELP FOR MANAGER", self.parent, self.name)
        print("self.managers", self.managers)
        print("self.commands", self.commands)

    def manager(self, help="", name=None):
        """Decorator for adding a sub-manager to this manager."""
        def decorator(func):
            _manager = Manager(func, help=help, name=name)
            self.managers[_manager.name] = _manager
            _manager.__doc__ = func.__doc__
            return _manager

        return decorator

    def command(self, help="", name=None):
        """Decorator for adding a command to this manager."""
        def decorator(func):
            _command = Command(func, help=help, name=name)
            self.commands[_command.name] = _command
            _command.__doc__ = func.__doc__
            return _command

        return decorator


def manager(help="", name=None):
    """Decorator for creating a root manager"""
    def decorator(func):
        _manager = Manager(func, help=help, name=name)
        _manager.__doc__ = func.__doc__
        return _manager

    return decorator
