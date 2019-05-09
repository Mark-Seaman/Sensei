from os.path import join
from os import environ

from bin.shell import shell_file_list


def count_files(filetype=None):
    if filetype:
        return str(len([f for f in files if '.'+filetype in f]))
    return str(len(files))


files = shell_file_list(join(environ['HOME'], 'Angular'))


def angular_css_files_test():
    return count_files('css')


def angular_typescript_files_test():
    return count_files('ts')


def angular_html_files_test():
    return count_files('html')


def angular_files_test():
    return count_files()

