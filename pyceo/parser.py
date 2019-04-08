

def parse_args(cliargs):
    """Parse the command line arguments and return a list of the positional
    arguments and a dictionary with the named ones.

        >>> parse_args(["abc", "def", "-w", "3", "--foo", "bar", "-narf=zort"])
        (['abc', 'def'], {'w': '3', 'foo': 'bar', 'narf': 'zort'})

        >>> parse_args(["-abc"])
        ([], {'abc': True})

        >>> parse_args(["-f", "1", "-f", "2", "-f", "3"])
        ([], {'f': ['1', '2', '3']})

    """
    # Split the "key=arg" arguments
    largs = []
    for arg in cliargs:
        if "=" in arg:
            key, arg = arg.split("=")
            largs.append(key)
        largs.append(arg)

    args = []
    flags = []
    kwargs = {}
    key = None
    for sarg in largs:
        if is_key(sarg):
            if key is not None:
                flags.append(key)
            key = sarg.strip("-")
            continue

        if not key:
            args.append(sarg)
            continue

        value = kwargs.get(key)
        if value:
            if isinstance(value, list):
                value.append(sarg)
            else:
                value = [value, sarg]
            kwargs[key] = value
        else:
            kwargs[key] = sarg

    # Get the flags
    if key:
        flags.append(key)
    # An extra key whitout a value is a flag if it hasn"t been used before.
    # Otherwise is a typo.
    for flag in flags:
        if not kwargs.get(flag):
            kwargs[flag] = True

    return args, kwargs


def is_key(sarg):
    """Check if `sarg` is a key (eg. -foo, --foo) or a negative number (eg. -33).
    """
    if not sarg.startswith("-"):
        return False
    if sarg.startswith("--"):
        return True
    return not sarg.lstrip("-").isnumeric()
