from os import environ
from os.path import join
from bin.shell import check_files, check_shell_lines


def check_page(url, min=1, max=1):
    x = check_shell_lines('curl -s %s' % url, min, max)
    return x if x else 'OK - %s' % url


def unc_files_test():
    path = join(environ['HOME'], 'UNC')
    return check_files(path, 67, 67)


def unc_docs_test():
    path = join(environ['HOME'], 'Sensei', 'Documents', 'unc')
    return check_files(path, 57, 57)


def unc_site_test():
    return check_page('https://shrinking-world.com/unc/bacs200/02', 343, 343)

