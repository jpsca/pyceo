# -*- coding: utf-8 -*-
"""
# pyCEO

Create management scripts for your applications so you can do
things like `python manage.py runserver`.

It can also be nested for sub-commands.

------------
Copyright © 2011 by [Lúcuma labs] (http://lucumalabs.com).  
See `AUTHORS.md` for more details.  
License: [MIT License] (http://www.opensource.org/licenses/mit-license.php).

"""
from functools import reduce
import os
import re
import sys

from .helpers import *


__version__ = '0.9'

HELP_COMMANDS = ('help', 'h')


class Command(object):
    
    def __init__(self, func, pre=None):
        self.func = func
        self.pre = pre
        
        self.name = func.__name__
        description = func.__doc__ or ''
        description = smart_outdent(description)
        self.description = re.sub('\n', '\n      ', description)
    
    def run(self, args, kwargs):
        show_help = False
        if kwargs and not args:
            show_help = True
            for key in kwargs:
                if key not in HELP_COMMANDS:
                    show_help = False
                    break
        elif args and args[0] in HELP_COMMANDS:
            show_help = True
        
        if show_help:
            print self.get_help()
            return False
        
        if self.pre:
            self.pre(args, kwargs)
        
        self.func(*args, **kwargs)
        return True
    
    def get_help(self):
        shelp = [
            format_title('USAGE'), '\n',
            '  ', bold(self.name), '  ', self.description,
        ]
        return ''.join(shelp)


class Manager(object):
    """Controller class for handling a set of commands.
    """
    
    def __init__(self, description=None, item_name='command', pre=None):
        """

        description
        :   The help message to use instead of the default one

        item_name
        :   How to call the commands in the help. Default 'command'.

        pre
        :   Execute this function before any command.

        """
        self.description = description
        self.item_name = item_name
        self.pre = pre

        self.commands = {}
        self.prog = ''
        self.default = None
    
    def command(self, func):
        """Decorator to register a function as a command.
            
            @manager.command
            def hello(name, url='http://google.com'):
                print "hello", name, 'at', url
            
            >>> python manager.py hello -name Larry
            Hello Larry at http://google.com
            
            >>> python manager.py hello -name Steve -url bing.com
            Hello Steve at bing.com
            
            >>> python manager.py hello nurse "Burbank, California"
            Hello nurse at Burbank, California
            
            >>> python manager.py hello world lucumalabs.com
            Hello world at lucumalabs.com
        
        """
        if isinstance(func, type):
            func = func()
        self.commands[func.__name__] = Command(func, self.pre)
        return func
    
    def subcommand(self, name, *args, **kwargs):
        manager = Manager(*args, **kwargs)
        self.commands[name] = manager
        return manager
    
    def run(self, default=None):
        """Parse the command line arguments.
        
        default
        :   Name of default command to run if no arguments are passed.

        """
        argv = sys.argv
        prog = argv[0] 
        self.prog = os.path.split(prog)[1]
        self.default = default
        try:
            name = argv[1]
            lsargs = argv[2:]
        except IndexError:
            name = default
            lsargs = []
        
        if (not name) or (name.strip('-') in HELP_COMMANDS):
            print self.get_help()
            return False
        
        command = self.find_command(name)
        
        if command is None:
            item_name = self.item_name.capitalize()
            print '%s "%s" not found' % (item_name, name)
            print self.get_help()
            return False
        
        args, kwargs = parse_args(lsargs)
        command = self.find_subcommand(command, args)
        if command:
            return command.run(args, kwargs)
    
    def find_subcommand(self, command, args):
        while isinstance(command, self.__class__):
            if not args:
                print command.get_help()
                return
            
            name = args[0]
            _command = command.find_command(name)

            if _command is None:
                item_name = command.item_name.capitalize()
                print '%s "%s" not found' % (item_name, name)
                print command.get_help()
                return
            command = _command
            args.remove(name)
        
        return command
    
    def find_command(self, name):
        command = self.commands.get(name)
        if command:
            return command
        
        for n, c in self.commands.items():
            if n.startswith(name):
                return c
    
    def get_help(self):
        item_name = self.item_name
        shelp = []

        # Usage help
        if self.description:
            shelp.extend([
                format_title('USAGE'), '\n',
                '  ', self.description
            ])
        else:
            shelp.extend([
                format_title('USAGE'), '\n',
                '  %s %s [OPTIONS]\n' % (self.prog, item_name),
                '  %s %s\n' % (self.prog, HELP_COMMANDS[0])
            ])
    
        # Available commands
        shelp.append(format_title(item_name.upper()))
        chelp = []
        for name, command in self.commands.items():
            args = (
                ' ' if name != self.default else '*',
                bold(name),
                command.description
            )
            chelp.append('\n%s %s  %s' % args)

        shelp.append('\n\n'.join(chelp))
        
        return ''.join(shelp)

