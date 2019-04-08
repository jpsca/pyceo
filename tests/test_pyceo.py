# import pyceo


# def set_up_stdout():
#     sys.stdout = StringIO()


# def restore_stdout():
#     sys.stdout = sys.__stdout__


# def test_command_args():
#     set_up_stdout()
#     manager = Manager()

#     @manager.command
#     def hello(name='fred'):
#         print "hello", name

#     sys.argv = ['manage.py', 'hello', '-name=joe']
#     manager.run()
#     result = sys.stdout.getvalue()
#     assert 'hello joe\n' == result
#     restore_stdout()


# def test_no_command():
#     set_up_stdout()
#     manager = Manager()

#     @manager.command
#     def hello():
#         print 'hello world'

#     @manager.command
#     def bye():
#         print 'goodbye'

#     assert 'hello' in manager.commands
#     assert 'bye' in manager.commands

#     sys.argv = ['manage.py']
#     manager.run()
#     assert '= USAGE =' in sys.stdout.getvalue()
#     restore_stdout()


# def test_default_command():
#     set_up_stdout()
#     manager = Manager()

#     @manager.command
#     def hello():
#         print 'hello world'

#     @manager.command
#     def bye():
#         print 'goodbye'

#     assert 'hello' in manager.commands
#     assert 'bye' in manager.commands

#     sys.argv = ['manage.py']
#     manager.run(default='hello')
#     assert 'hello world\n' == sys.stdout.getvalue()

#     sys.stdout = StringIO()
#     sys.argv = ['manage.py']
#     manager.run(default='bye')
#     assert 'goodbye\n' == sys.stdout.getvalue()
#     restore_stdout()


# def test_command_no_args():
#     set_up_stdout()
#     manager = Manager()

#     @manager.command
#     def hello():
#         print 'hello world'

#     @manager.command
#     def bye():
#         print 'goodbye'

#     sys.argv = ['manage.py', 'hello']
#     manager.run()
#     assert 'hello world\n' == sys.stdout.getvalue()

#     sys.stdout = StringIO()
#     sys.argv = ['manage.py', 'bye']
#     manager.run()
#     assert 'goodbye\n' == sys.stdout.getvalue()

#     sys.stdout = StringIO()
#     sys.argv = ['manage.py', 'bye']
#     manager.run(default='hello')
#     assert 'goodbye\n' == sys.stdout.getvalue()
#     restore_stdout()


# def test_command_wrong_args():
#     set_up_stdout()
#     manager = Manager()

#     @manager.command
#     def hello(name):
#         print "hello", name

#     @manager.command
#     def kwargs(**kwargs):
#         pass

#     @manager.command
#     def args(*args):
#         pass

#     @manager.command
#     def dontcare(*args, **kwargs):
#         pass

#     sys.argv = ['manage.py', 'hello', '-n', 'joe']
#     with pytest.raises(TypeError):
#         manager.run()

#     sys.argv = ['manage.py', 'hello', '-name', 'joe', '-foo', 'bar']
#     with pytest.raises(TypeError):
#         manager.run()

#     sys.argv = ['manage.py', 'kwargs', '-n', 'joe']
#     manager.run()

#     sys.argv = ['manage.py', 'kwargs', 'joe']
#     with pytest.raises(TypeError):
#         manager.run()

#     sys.argv = ['manage.py', 'args', 'joe']
#     manager.run()

#     sys.argv = ['manage.py', 'args', '-n', 'joe']
#     with pytest.raises(TypeError):
#         manager.run()

#     sys.argv = ['manage.py', 'dontcare', 'joe']
#     manager.run()

#     sys.argv = ['manage.py', 'dontcare', '-n', 'joe']
#     manager.run()
#     restore_stdout()


# def test_subcommand():
#     set_up_stdout()
#     manager = Manager()
#     printer = manager.subcommand('hello', 'prints hello X', item_name='printer')

#     @printer.command
#     def nurse():
#         print 'Hellooo nurse'

#     sys.argv = ['manage.py', 'hello', 'nurse']
#     manager.run()
#     assert 'Hellooo nurse\n' == sys.stdout.getvalue()
#     restore_stdout()


# def test_subcommand_help():
#     set_up_stdout()
#     manager = Manager()
#     printer = manager.subcommand('hello', 'prints hello X', item_name='printer')

#     @printer.command
#     def nurse():
#         print 'Hellooo nurse'

#     sys.argv = ['manage.py', 'hello']
#     manager.run()
#     result = sys.stdout.getvalue()
#     assert 'prints hello X' in result
#     restore_stdout()

# def test_help():
#     set_up_stdout()
#     manager = Manager()

#     @manager.command
#     def hello(name):
#         "Prints your name"
#         pass

#     sys.argv = ['manage.py', 'help']
#     manager.run()
#     assert 'Prints your name' in sys.stdout.getvalue()

#     sys.stdout = StringIO()
#     sys.argv = ['manage.py']
#     manager.run()
#     assert 'Prints your name' in sys.stdout.getvalue()
#     restore_stdout()
