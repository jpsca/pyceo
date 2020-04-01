import textwrap


__all__ = ("Command", "HELP_COMMANDS", "get_doc")

HELP_COMMANDS = ("help", "h")


def get_doc(func):
    """Extract and dedent the __doc__ of a function.

    Unlike `textwrap.dedent()` it also works when the first line
    is not indented.
    """
    doc = func.__doc__
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


class Command(object):
    """
    """

    manager = None

    def __init__(self, func, help="", name=None):
        self.func = func
        self.name = name or func.__name__

        self.description = (get_doc(func) or help).strip()
        self.help = help or self.description.split("\n", 1)[0]

        # @param or @option decorators could have already been executed
        # to the bare function
        self.params = getattr(func, "params", [])
        self.options = getattr(func, "options", {})

    def __call__(self, *args, catch_errors=True, **opts):
        try:
            return self.func(*args, **opts)
        except KeyboardInterrupt:
            print()
        except TypeError as error:
            if not catch_errors:
                raise
            self.manager.show_error(error.args[0])

    def _filter_options(self, opts):
        parsed_opts = {}

        for key, value in opts.items():
            _option = self.options.get(key)
            if not _option:
                continue
            if _option.type is not None:
                try:
                    value = _option.type(value)
                except (TypeError, ValueError):
                    self.manager.show_error(f"Wrong argument for `{key}`")
                    raise
            parsed_opts[key] = value

        return parsed_opts

    def run(self, *args, catch_errors=True, **opts):
        for key in opts:
            if key.lstrip("-") in HELP_COMMANDS:
                self.show_help()
                return

        try:
            opts = self._filter_options(opts)
        except (TypeError, ValueError):
            return

        return self(*args, catch_errors=catch_errors, **opts)

    def show_help(self):
        self.manager.show_help_command(self)
