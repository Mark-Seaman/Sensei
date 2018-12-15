#!/usr/bin/env python

from os import environ, system
from os.path import  join
from platform import node
from sys import argv

from switches import APP_PORT


# ------------------------------
# Command Interpreter

def web_command(args):
    '''Execute all of the web specific webs'''
    cmd = args[0] if args else 'mybook'

    if cmd=='dev':
        web('http://localhost:%s/%s' % (APP_PORT, '/'.join(args[1:])))

    elif cmd=='github':
        web('https://github.com/Shrinking-World/MyBook.git')

    elif cmd=='mybook':
        web('http://markseaman.org')

    elif cmd=='test':
        web('http://localhost:%s/%s' % (APP_PORT, 'superuser/tests'))

    elif cmd=='time':
        web('http://markseaman.info')

    else:
        web_help()


def web_help():
    '''Show all the web webs and their usage.'''
    print('''
    usage:  web cmd [args]

    cmd:

        dev         - Local website
        github      - Go the Github site
        mybook      - My Book Online website
        test        - Show local test results
        time        - Track time for project

            ''')


def web(page):
    '''Open a web page in Google Chrome'''
    url = page
    if not page.startswith('http://') and not page.startswith('https://'):
        url = 'http://' + page
    # Use the correct invocation
    if 'iMac' in node() or 'mac' in node():
        system('open -a "Google Chrome" '+url)
    else:
        system('rbg google-chrome '+url)


def web_path(topic=None):
    path = environ['pb']
    if topic:
        path = join(path,topic)
    return path



'''
Create a script that can be run from the shell
'''
if __name__=='__main__':
    web_command(argv)

