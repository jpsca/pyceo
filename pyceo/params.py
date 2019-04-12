

class Param(object):

    __slots__ = ("name", "full_name", "help")

    def __init__(self, name, help):
        name = name.lstrip("-")
        self.name = name.split(" ", 1)[0]
        self.full_name = name
        self.help = help

    @property
    def title(self):
        if len(self.name) == 1:
            return "-" + self.full_name
        return "--" + self.full_name


def param(name, help=""):
    """Decorator that add a parameter to the wrapped command or function."""
    def decorator(func):
        params = getattr(func, "params", [])
        _param = Param(name, help)
        # Insert at the beginning so the apparent order is preserved
        params.insert(0, _param)
        func.params = params
        return func

    return decorator


def option(name, help=""):
    """Decorator that add an option to the wrapped command or function."""
    def decorator(func):
        options = getattr(func, "options", [])
        _option = Param(name, help)
        # Insert at the beginning so the apparent order is preserved
        options.insert(0, _option)
        func.options = options
        return func

    return decorator
