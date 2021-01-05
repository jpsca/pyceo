import colorama
from colorama import Style, Fore, Back


colorama.init()

STYLE_ALIASES = {
    "<b>": "<op:bright>",
    "</b>": "</op>",
}


def style(text, aliases=STYLE_ALIASES):
    if aliases:
        for tag, value in aliases.items():
            text = text.replace(tag, value)

    return (
        text.replace("<op:bright>", Style.BRIGHT)
        .replace("<op:dim>", Style.DIM)
        .replace("</op>", Style.NORMAL)

        .replace("<fg:black>", Fore.BLACK)
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

        .replace("<bg:black>", Back.BLACK)
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
