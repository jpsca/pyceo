import textwrap

import colorama
from colorama import Style, Fore, Back


__all__ = ("DEFAULT_STYLES", "HelpMixin", "echo", "styled")

colorama.init()

DEFAULT_STYLES = {
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


class HelpMixin(object):

    MIN_COL_SIZE = 12
    INDENT_WITH = " "
    styles = DEFAULT_STYLES

    def echo(self, text):
        echo(text, styles=self.styles)

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
            textwrap.dedent(self.intro), "\n",
            textwrap.dedent(f"""
            <h2>Usage</h2>
              {self.parent} <command> [<arg1>]...[<argN>] [--<op1>]...[--<opN>]

              All commands can be run with -h (or --help) for more information.

            <h2>Available Commands</h2>""")
        ]

        for header, commands in self.command_groups.items():
            msg.append(self.help_commands_group(header, commands.values()))

        return "".join(msg)

    def help_commands_group(self, header, commands):
        msg = ["\n"]
        if header:
            msg.append(f" <h3>{header}</h3>\n")

        col_size = self.get_col_size(commands)
        for cmd in commands:
            msg.append(self.help_line_item(cmd.name, cmd.help, col_size))

        return "".join(msg)

    def help_line_item(self, name, cmd_help, col_size=MIN_COL_SIZE):
        cmd_help = cmd_help.strip().split("\n")[0]
        return f"  <cmd>{name.ljust(col_size)}</cmd> {cmd_help}\n"

    def help_command(self, cmd):
        msg = ["\n<h2>Usage</h2>\n"]
        usage = f"  {self.parent} {cmd.name}"
        if cmd.params:
            usage += " [<arg1>]...[<argN>]"
        if cmd.options:
            usage += " [--<op1>]...[--<opN>]"
        msg.append(usage + "\n")

        if cmd.params:
            msg.append("\n<h2>Arguments</h2>\n")

            col_size = self.get_col_size(cmd.params)
            for param in cmd.params:
                msg.append(self.help_line_item(param.name, param.help, col_size))

        if cmd.options:
            msg.append("\n<h2>Options</h2>\n")
            # Reversed to preserve the apparent order
            options = [op for op in reversed([value for value in cmd.options.values()])]
            col_size = self.get_col_size(options, attr="header")
            for op in options:
                msg.append(self.help_line_item(op.header, op.help, col_size))

        msg.append("\n<h2>Description</h2>\n")
        msg.append(cmd.description)

        return "".join(msg) + "\n"


def echo(*texts, sep=" ", styles=DEFAULT_STYLES):
    text = sep.join(texts)
    print(styled(text, styles))


def styled(text, styles=DEFAULT_STYLES):
    # Custom styles
    for tag, value in styles.items():
        text = text.replace(tag, value)

    text = (
        text.replace("<op:bright>", Style.BRIGHT)
        .replace("<op:dim>", Style.DIM)
        .replace("</op>", Style.RESET_ALL)
    )

    text = (
        text.replace("<fg:black>", Fore.BLACK)
        .replace("<fg:red>", Fore.RED)
        .replace("<fg:green>", Fore.GREEN)
        .replace("<fg:yellow>", Fore.YELLOW)
        .replace("<fg:blue>", Fore.BLUE)
        .replace("<fg:magenta>", Fore.MAGENTA)
        .replace("<fg:cyan>", Fore.CYAN)
        .replace("<fg:white>", Fore.WHITE)
        .replace("<fg:lblack>", Fore.LIGHTBLACK_EX)
        .replace("<fg:lred>", Fore.LIGHTRED_EX)
        .replace("<fg:lgreen>", Fore.LIGHTGREEN_EX)
        .replace("<fg:lyellow>", Fore.LIGHTYELLOW_EX)
        .replace("<fg:lblue>", Fore.LIGHTBLUE_EX)
        .replace("<fg:lmagenta>", Fore.LIGHTMAGENTA_EX)
        .replace("<fg:lcyan>", Fore.LIGHTCYAN_EX)
        .replace("<fg:lwhite>", Fore.LIGHTWHITE_EX)
        .replace("</fg>", Fore.RESET)
    )

    text = (
        text.replace("<bg:black>", Back.BLACK)
        .replace("<bg:red>", Back.RED)
        .replace("<bg:green>", Back.GREEN)
        .replace("<bg:yellow>", Back.YELLOW)
        .replace("<bg:blue>", Back.BLUE)
        .replace("<bg:magenta>", Back.MAGENTA)
        .replace("<bg:cyan>", Back.CYAN)
        .replace("<bg:white>", Back.WHITE)
        .replace("<bg:lblack>", Back.LIGHTBLACK_EX)
        .replace("<bg:lred>", Back.LIGHTRED_EX)
        .replace("<bg:lgreen>", Back.LIGHTGREEN_EX)
        .replace("<bg:lyellow>", Back.LIGHTYELLOW_EX)
        .replace("<bg:lblue>", Back.LIGHTBLUE_EX)
        .replace("<bg:lmagenta>", Back.LIGHTMAGENTA_EX)
        .replace("<bg:lcyan>", Back.LIGHTCYAN_EX)
        .replace("<bg:lwhite>", Back.LIGHTWHITE_EX)
        .replace("</bg>", Back.RESET)
    )

    return text
