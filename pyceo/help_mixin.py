import textwrap
from inspect import isclass

from .helpers import echo


HELP_OPT = "help"
INDENT_WITH = "  "
COL_SIZE = 12


def get_doc(cmd):
    """Extract and dedent the __doc__ of a method/function.

    Unlike `textwrap.dedent()` it also works when the first line
    is not indented.
    """
    doc = cmd.__doc__
    if not doc:
        return ""

    # doc has only one line
    if "\n" not in doc:
        return doc

    # Only Python core devs write __doc__ like this
    if doc.startswith(("\n", "\\\n")):
        return textwrap.dedent(doc)

    # First line is not indented
    first, rest = doc.split("\n", 1)
    return first + "\n" + textwrap.dedent(rest)


class HelpMixin:

    @property
    def _commands(self):
        commands = {}
        for name in dir(self):
            if name.startswith("_"):
                continue
            cmd = getattr(self, name, None)
            if isclass(cmd):
                continue
            commands[name] = cmd
        return commands

    @property
    def _subcommands(self):
        subcommands = {}
        for name in dir(self):
            if name.startswith("_"):
                continue
            cls = getattr(self, name, None)
            if not isclass(cls):
                continue
            subcommands[name] = cls
        return subcommands

    @property
    def _indent(self):
        return INDENT_WITH * self._indent_level

    def _help(self, header=True):
        self._help_intro()
        self._help_header()
        self._help_body()
        print()

    def _help_intro(self):
        doc = get_doc(self)
        if doc:
            intro = textwrap.indent(doc.strip(), " ")
            echo(f"\n{intro}")

    def _help_header(self):
        echo("\n <fg:yellow>Usage:</fg>")
        echo(f" {self._indent}{self._parent} <command> [args] [options]\n")
        echo(
            f" {self._indent}"
            "Run any command with the --help option for more information."
        )
        echo("\n <fg:yellow>Available Commands:</fg>")

    def _help_body(self):
        for name, cmd in self._commands.items():
            self._help_list_command(name, cmd)
        for name, cls in self._subcommands.items():
            self._help_list_subcommand(name, cls)

    def _help_list_subcommand(self, name, cls):
        echo(f"\n {self._indent}<fg:cyan>{name.ljust(COL_SIZE)}</fg>")
        cli = self._init_subcommand(name, cls, indent_level=self._indent_level + 1)
        cli._help_body()

    def _help_list_command(self, name, cmd):
        doc = cmd.__doc__ or ""
        cmd_help = doc.strip().split("\n")[0]
        echo(f" {self._indent}<fg:lgreen>{name.ljust(COL_SIZE)}</fg> {cmd_help}")

    def _help_command(self, cmd):
        print()
        doc = get_doc(cmd)
        echo(textwrap.indent(doc, " "), aliases=None)
