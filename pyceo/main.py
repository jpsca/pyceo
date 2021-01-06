import sys
from inspect import isclass
from pathlib import Path

from .help_mixin import HelpMixin, HELP_OPT
from .helpers import echo
from .parser import parse_args


INDENT_START_LEVEL = 1


class Cli(HelpMixin):
    def __init__(self, *, parent="", indent_level=INDENT_START_LEVEL, **env):
        self._parent = parent
        self._indent_level = indent_level
        self._env = env

    def __call__(self, *, default=None):
        try:
            parent, *sysargs = sys.argv
            self._parent = Path(parent).stem
            args, opts = parse_args(sysargs)
            self._run(*args, **opts)
        except KeyboardInterrupt:
            print()

    # Private

    def _run(self, *args, **opts):
        cmd = None
        if not args:
            return self._help()

        name, *args = args
        cmd = getattr(self, name, None)
        if not cmd:
            return self._command_not_found(name)

        if isclass(cmd):
            return self._run_subcommand(name, cmd, args, opts)
        return self._run_command(cmd, args, opts)

    def _command_not_found(self, name):
        echo(f"\n💥 <fg:red><b>ERROR:</b> Command `{name}` not found</fg> 💥 ")
        self._help()

    def _init_subcommand(self, name, cls, indent_level=INDENT_START_LEVEL):
        return cls(
            parent=f"{self._parent} {name}",
            indent_level=indent_level,
            **self._env
        )

    def _run_subcommand(self, name, cls, args, opts):
        cli = self._init_subcommand(name, cls)
        if not args:
            if not opts or opts == {HELP_OPT: True}:
                return cli._help()
        return cli._run(*args, **opts)

    def _run_command(self, cmd, args, opts):
        if HELP_OPT in opts:
            return self._help_command(cmd)
        return cmd(*args, **opts)
