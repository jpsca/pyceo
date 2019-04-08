

class Param(object):

    __slots__ = ("name", "help")

    def __init__(self, name, help):
        self.name = name
        self.help = help


def param(name, help=""):
    """Decorator that add a parameter to the wrapped command or function."""
    def decorator(func):
        params = getattr(func, "params", [])
        _param = Param(name, help)
        params.append(_param)
        func.params = params
        return func

    return decorator


def option(name, help=""):
    """Decorator that add an option to the wrapped command or function."""
    def decorator(func):
        options = getattr(func, "options", [])
        _option = Param(name, help)
        options.append(_option)
        func.options = options
        return func

    return decorator
