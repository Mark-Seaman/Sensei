from os import environ, system
from os.path import join

from shell import banner, file_tree_list, read_file


# ------------------------------
# Command Interpreter

def i_command(options):
    if options:
        cmd = options[0]
        args = options[1:]
        if cmd=='edit':
            i_edit(args)
        elif cmd=='list':
            i_list(args)
        else:
            i_list(options)
    else:
        i_help()


def i_help(args=None):
    print('''
        i Command

        usage: x i [COMMAND] [Idea to save]

        COMMAND:

            edit  - edit the ideas file
            list  - list the ideas
        ''')


# ------------------------------
# Functions

def doc_path():
    return join(environ['p'], 'Documents', 'info', 'ideas')

def i_add(args):
    if args:
        open(doc_path(), 'a').write(' '.join(args) + '\n')
    
def i_edit(args):
    i_add(args)
    system('e '+doc_path())


def i_list(args):
    i_add(args)
    print (open(doc_path()).read())

    