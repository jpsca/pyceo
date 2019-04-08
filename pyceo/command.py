import textwrap


__all__ = ("Command", "HELP_COMMANDS")

HELP_COMMANDS = ("help", "h")


class Command(object):

    def __init__(self, func, help="", name=None):
        self.func = func
        self.name = name or func.__name__
        self.description = textwrap.dedent(func.__doc__ or "")
        self.help = help

        # @param or @option decorators could have already been executed
        # to the bare function
        self.params = getattr(func, "params", [])
        self.options = getattr(func, "options", [])

    def __call__(self, *args, **opts):
        return self.func(*args, **opts)

    def run(self, *args, **opts):
        for key in opts:
            if key.lstrip("-") in HELP_COMMANDS:
                self.show_help()
                return

        len_args = len(args)
        len_params = len(self.params)
        if len_args != len_params:
            self.show_error("Invalid number of arguments", args, opts)
            self.show_help()
            return

        return self(*args, **opts)

    def show_error(self, msg, args, opts):
        print("\nERROR:", msg)
        print("Recieved:")
        print("  args:  ", args)
        print("  opts:", opts)

    def show_help(self):
        print(f"\nHELP FOR COMMAND {self.name}")
        print("self.params", self.params)
        print("self.options", self.options)
