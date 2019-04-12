"""
# pyceo.main

Create management scripts for your applications so you can do
things like `python manage.py runserver`.

"""
import sys

from .command import Command, HELP_COMMANDS
from .parser import parse_args
from .help_mixin import HelpMixin


__all__ = ("Manager", )


class Manager(HelpMixin):

    parent = ""

    def __init__(self, intro=""):
        self.intro = intro
        self.commands = {}
        self.command_groups = {None: []}

    def __call__(self, *args, **opts):
        return self.func(*args, **opts)

    def run(self, default=None):
        """Parse the command line arguments.

        default:
            Name of default command to run if no arguments are passed.

        """
        self.parent, *sys_args = sys.argv
        cmd_name = default
        if sys_args:
            cmd_name, *sys_args = sys_args

        if cmd_name is None or cmd_name.lstrip("-") in HELP_COMMANDS:
            self.show_help_root()
            return

        command = self.commands.get(cmd_name)
        if command is None:
            self.show_error(f"command `{cmd_name}` not found")
            self.show_help_root()
            return

        args, opts = parse_args(sys_args)
        return command.run(*args, **opts)

    def command(self, group=None, help="", name=None):
        """Decorator for adding a command to this manager."""
        def decorator(func):
            return self.add_command(func, group=group, help=help, name=name)
        return decorator

    def add_command(self, func, group=None, help="", name=None):
        if isinstance(func, Command):
            help = help or func.help
            name = name or func.help
            func = func.func

        cmd = Command(func, group=group, help=help, name=name)
        cmd.manager = self
        cmd.__doc__ = func.__doc__

        self.commands[cmd.name] = cmd

        group = None
        if ":" in cmd.name:
            group = cmd.name.split(":", 1)[0]
        self.command_groups.setdefault(group, [])
        self.command_groups[group].append(cmd)

        return cmd

    def add_commands(self, cmds, group=None):
        for cmd in cmds:
            self.add_command(cmd, group=group)
