# -*- coding: utf-8 -*-
"""
# pyCEO.helpers

"""
import getpass
import re
import string


def _is_a_key(sarg):
    """Check if `sarg` is a key (eg. -foo, --foo) or a value (eg. -33).
    """
    if not sarg.startswith('-'):
        return False
    try:
        float(sarg)
        return False
    except ValueError:
        return True


def parse_args(largs_):
    """Parse the command line arguments and return a list of the positional
    arguments and a dictionary with the named ones.
        
        >>> parse_args(['abc', 'def', '-w', '3', '--foo', 'bar', '-narf=zort'])
        (['abc, 'def'], {'w': '3', 'foo': 'bar', 'narf': 'zort'})
        >>> parse_args(['-abc'])
        ([], {'abc': True})
        >>> parse_args(['-f', '1', '-f', '2', '-f', '3'])
        ([], {'f': ['1', '2', '3']})
    
    """
    # Split the 'key=arg' arguments
    largs = []
    for arg in largs_:
        if '=' in arg:
            key, arg = arg.split('=')
            largs.append(key)
        largs.append(arg)
    
    args = []
    flags = []
    kwargs = {}
    key = None
    for sarg in largs:
        if _is_a_key(sarg):
            if key is not None:
                flags.append(key)
            key = sarg.strip('-')
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
    # An extra key whitout a value is a flag if it hasn't been used before.
    # Otherwise is a typo.
    for flag in flags:
        if not kwargs.get(flag):
            kwargs[flag] = True
    
    return args, kwargs


MAX_INDENT = 80

def smart_outdent(text):
    """Removes the external indentation of the text without loosing the
    internal one."""
    text = text.expandtabs(4).rstrip()
    all_indents = re.findall(r'\n+(\s+)\w', text)
    len_indent = MAX_INDENT if all_indents else 0
    for indent in all_indents:
        len_indent = min(len_indent, len(indent))
    ext_indent = ' ' * len_indent
    return text.replace('\n' + ext_indent, '\n').lstrip()


def esc(*codes):
    return "\x1b[%sm" % (";".join([str(c) for c in codes]))


def bold(text):
    return esc(1) + text + esc(22)


def format_title(text, ll=52):
    return '\n= %s %s\n' % (text, '=' * ll)


def prompt(text, default=None, _test=None):
    """Ask a question via raw_input() and return their answer.
    
    param text: prompt text
    param default: default value if no answer is provided.
    """
    
    text += ' [%s]' % default if default else ''
    while True:
        if _test is not None:
            print text
            resp = _test
        else:
            resp = raw_input(text)
        if resp:
            return resp
        if default is not None:
            return default


def prompt_pass(text, default=None, _test=None):
    """Prompt the user for a secret (like a password) without echoing.
    
    :param name: prompt text
    :param default: default value if no answer is provided.
    """
    
    text += ' [%s]' % default if default else ''
    while True:
        if _test is not None:
            print text
            resp = _test
        else:
            resp = getpass.getpass(text)
        if resp:
            return resp
        if default is not None:
            return default


def prompt_bool(text, default=False, yes_choices=None, no_choices=None,
      _test=None):
    """Ask a yes/no question via raw_input() and return their answer.
    
    :param text: prompt text
    :param default: default value if no answer is provided.
    :param yes_choices: default 'y', 'yes', '1', 'on', 'true', 't'
    :param no_choices: default 'n', 'no', '0', 'off', 'false', 'f'
    """
    
    yes_choices = yes_choices or ('y', 'yes', 't', 'true', 'on', '1')
    no_choices = no_choices or ('n', 'no', 'f', 'false', 'off', '0')
    
    default = yes_choices[0] if default else no_choices[0]
    while True:
        if _test is not None:
            print text
            resp = _test
        else:
            resp = prompt(text, default)
        if not resp:
            return default
        resp = str(resp).lower()
        if resp in yes_choices:
            return True
        if resp in no_choices:
            return False


def prompt_choices(text, choices, default=None, resolver=string.lower,
      _test=None):
    """Ask to select a choice from a list, and return their answer.
    
    :param text: prompt text
    :param choices: list or tuple of available choices. Choices may be
        strings or (key, value) tuples.
    :param default: default value if no answer provided.
    """
    
    _choices = []
    options = []
    
    for choice in choices:
        if isinstance(choice, basestring):
            options.append(choice)
        else:
            options.append("%s [%s]" % (choice[1], choice[0]))
            choice = choice[0]
        _choices.append(choice)
    
    text += ' – (%s)' % ', '.join(options)
    while True:
        if _test is not None:
            print text
            resp = _test
        else:
            resp = prompt(text, default)
        resp = resolver(resp)
        if resp in _choices:
            return resp
        if default is not None:
            return default

