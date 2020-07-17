def ask(text, default=None, options=None):
    """Ask a question via input() and return their answer.

    Parameters:

    - text (str): Question text
    - default (any): Default value if no answer is provided.
    - options (str): Options to display
    """
    ops = options or default
    text += f" [{str(ops)}] " if ops else ""
    while True:
        resp = input(text)
        if resp:
            return resp
        if default is not None:
            return default


def confirm(text, default=False, yes_choices=None, no_choices=None):
    """Ask a yes/no question via pycero.ask() and return their answer.

    Parameters:

    - text (str): prompt text
    - default (bool): default value if no answer is provided.
    - yes_choices (list): default 'y', 'yes', '1', 'on', 'true', 't'
    - no_choices (list): default 'n', 'no', '0', 'off', 'false', 'f'

    """
    yes_choices = yes_choices or ('y', 'yes', 't', 'true', 'on', '1')
    no_choices = no_choices or ('n', 'no', 'f', 'false', 'off', '0')

    default_value = yes_choices[0] if default else no_choices[0]
    if default is None:
        options = f"{yes_choices[0]}|{no_choices[0]}"
    else:
        if default:
            options = f"{yes_choices[0].title()}|{no_choices[0]}"
        else:
            options = f"{yes_choices[0]}|{no_choices[0].title()}"

    while True:
        resp = ask(text, default=default_value, options=options)
        if default is not None:
            resp = resp or str(default)
        resp = resp.lower()
        if resp in yes_choices:
            return True
        if resp in no_choices:
            return False

