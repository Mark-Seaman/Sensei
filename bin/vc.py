from os import chdir, environ, system
from os.path import exists, join

from shell import shell


# ------------------------------
# Command Interpreter

def vc_command(options):
    if options:
        cmd = options[0]
        args = options[1:]
        chdir(environ['p'])
        if cmd == 'commit':
            vc_commit(args)
        elif cmd == 'diff':
            vc_diff(args)
        elif cmd == 'log':
            vc_log(args)
        elif cmd == 'pull':
            vc_pull(args)
        elif cmd == 'push':
            vc_push(args)
        elif cmd == 'status':
            vc_status(args)
        else:
            vc_help(args)
    else:
        vc_help(options)


def vc_help(args=None):
    print('''
        vc Command

        usage: x vc COMMAND [ARGS]

        COMMAND:

            commit  - update all local changes in git
            diff    - show uncommitted changes
            log     - show the log on the production server
            pull    - pull all changes from repo
            push    - push all changes to repo
            status  - show git status

        ''')


# ------------------------------
# Functions

def git_cmd(cmd):
    system(cmd + git_filter())


def git_filter():
    x = ['"up to date"', 'up-to-date', 'nothing', '"no changes"', 
        '"branch master"', '"git add"', '"git checkout"']
    return '|grep -v ' + '|grep -v '.join(x)


def vc_commit(args):
    for d in vc_dirs():
        comment = ' '.join(args)
        cmd = 'echo commit %s && cd %s && git add -A . && git commit -m "%s"'
        git_cmd(cmd % (d, d, comment))
    vc_push(args)


def vc_diff(args):
    for d in vc_dirs():
        cmd = 'echo diff %s && cd %s && git diff --color'
        git_cmd(cmd % (d, d))


def vc_dirs():
    home   = environ['p']
    doc    = join(environ['p'], 'Documents')
    guide  = join(environ['HOME'], 'Archive')
    unc    = join(environ['unc'])
    dirs   = [home, doc, unc]
    dirs   = [d for d in dirs if exists(d)]
    return dirs


def vc_log(args):
    for d in vc_dirs():
        cmd = 'echo log %s && cd %s && git log --name-only'
        git_cmd(cmd %(d, d))


def vc_pull(args):
    for d in vc_dirs():
        cmd = 'echo pull %s && cd %s && git pull'
        git_cmd(cmd % (d, d))


def vc_push(args):
    for d in vc_dirs():
        cmd = 'echo push %s && cd %s && git pull %s; git push'
        git_cmd(cmd % (d, d, git_filter()))


def vc_status(args):
    for d in vc_dirs():
        cmd = 'echo status %s && cd %s && git status'
        git_cmd(cmd % (d, d))
