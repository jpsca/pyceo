import textwrap

import colorama
from colorama import Fore, Style


colorama.init()


class HelpMixin(object):

    MIN_COL_SIZE = 12
    INDENT_WITH = " "

    styles = {
        "<h2>": "<op:bright><fg:yellow>",
        "</h2>": "</op></fg>",

        "<h3>": "<fg:cyan>",
        "</h3>": "</fg>",

        "<b>": "<op:bright>",
        "</b>": "</op>",

        "<cmd>": "<fg:lgreen>",
        "</cmd>": "</fg>",

        "<error>": "<op:bright><fg:red>",
        "</error>": "</op></fg>",
    }

    def echo(self, txt):
        print(styled(txt, self.styles))

    def show_error(self, msg):
        error_msg = f"ERROR: {msg}"
        width = len(error_msg.split("\n", 1)[0]) + 1
        line = "—" * width

        msg = f"<error>{line}\n{error_msg}\n{line}</error>"
        msg = textwrap.indent(msg, self.INDENT_WITH)
        self.echo(msg)

    def get_col_size(self, items, attr="name"):
        attrs = list(map(lambda it: len(getattr(it, attr)), items))
        if not attrs:
            return self.MIN_COL_SIZE
        attrs.append(self.MIN_COL_SIZE)
        return max(*attrs)

    def show_help_root(self):
        msg = self.help_root()
        msg = textwrap.indent(msg, self.INDENT_WITH)
        self.echo(msg)

    def show_help_command(self, cmd):
        msg = self.help_command(cmd)
        msg = textwrap.indent(msg, self.INDENT_WITH)
        self.echo(msg)

    def help_root(self):
        msg = [
            textwrap.dedent(f"""
            {self.intro}

            <h2>Usage</h2>
              {self.parent} <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

              All commands can be run with -h (or --help) for more information.

            <h2>Available Commands</h2>""")
        ]

        for title, commands in self.command_groups.items():
            msg.append(self.help_commands_group(title, commands))

        return "".join(msg)

    def help_commands_group(self, title, commands):
        msg = ["\n"]
        if title:
            msg.append(f" <h3>{title}</h3>\n")

        col_size = self.get_col_size(commands)
        for cmd in commands:
            msg.append(self.help_line_item(cmd.name, cmd.help, col_size))

        return "".join(msg)

    def help_line_item(self, name, help, col_size=MIN_COL_SIZE):
        return f"  <cmd>{name.ljust(col_size)}</cmd> {help}\n"

    def help_command(self, cmd):
        msg = ["\n<h2>Usage</h2>\n"]
        usage = f"  {self.parent} {cmd.name}"
        if cmd.params:
            usage += " [<arg1>]...[<argN>]"
        if cmd.options:
            usage += " [--<op1>]...[--<opN>]"
        msg.append(usage + "\n")

        if cmd.params:
            msg.append("\n<h2>Parameters</h2>\n")

            col_size = self.get_col_size(cmd.params)
            for param in cmd.params:
                msg.append(self.help_line_item(param.name, param.help, col_size))

        if cmd.options:
            msg.append("\n<h2>Options</h2>\n")

            col_size = self.get_col_size(cmd.options, attr="title")
            for op in cmd.options:
                msg.append(self.help_line_item(op.title, op.help, col_size))

        msg.append("\n<h2>Description</h2>\n")
        msg.append(cmd.description)

        return "".join(msg) + "\n"


def styled(text, styles):
    # Custom styles
    for tag, value in styles.items():
        text = text.replace(tag, value)

    text = text \
        .replace("<op:bright>", Style.BRIGHT) \
        .replace("<op:dim>", Style.DIM) \
        .replace("</op>", Style.RESET_ALL)

    text = text \
        .replace("<fg:black>", Fore.BLACK) \
        .replace("<fg:red>", Fore.RED) \
        .replace("<fg:green>", Fore.GREEN) \
        .replace("<fg:yellow>", Fore.YELLOW) \
        .replace("<fg:blue>", Fore.BLUE) \
        .replace("<fg:magenta>", Fore.MAGENTA) \
        .replace("<fg:cyan>", Fore.CYAN) \
        .replace("<fg:white>", Fore.WHITE) \
        .replace("<fg:lblack>", Fore.LIGHTBLACK_EX) \
        .replace("<fg:lred>", Fore.LIGHTRED_EX) \
        .replace("<fg:lgreen>", Fore.LIGHTGREEN_EX) \
        .replace("<fg:lyellow>", Fore.LIGHTYELLOW_EX) \
        .replace("<fg:lblue>", Fore.LIGHTBLUE_EX) \
        .replace("<fg:lmagenta>", Fore.LIGHTMAGENTA_EX) \
        .replace("<fg:lcyan>", Fore.LIGHTCYAN_EX) \
        .replace("<fg:lwhite>", Fore.LIGHTWHITE_EX) \
        .replace("</fg>", Fore.RESET)

    return text
