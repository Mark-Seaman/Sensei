from django.utils.timezone import now
from os.path import exists, isdir, isfile, join
from os import  listdir, walk
from subprocess import Popen, PIPE
from sys import version_info

from bin.shell import read_file, word_count


# Read the markdown document and convert it to HTML
def doc_html(doc):
    return markdown_to_html(read_markdown(doc))


# Create a list of document links (doc, title) for one directory
def doc_list(path):

    def doc_entry(path, f):
        return doc_title(join(path, f)), f

    return [doc_entry(path, f) for f in list_files(path)]


def count_words(directory):
    matches = []
    for dirname, dirnames, filenames in walk(directory):
        for filename in filenames:
            base = dirname.replace(directory + '/', '')
            matches.append((filename, join(base, filename)))
    for m in matches:
        print('%-20s %s' % (m[0], m[1]))

# Create a list of document links (doc, title)
def doc_tree(doc):

    def bullet_indent(n):
        return '    ' * n + '* '

    def append_files(directory, indents):
        file_words = 0
        for fname in sorted(listdir(directory)):
            if isfile(join(directory, fname)):
                words = word_count(read_file(join(directory, fname)))
                file_words += words
                dname = directory.replace('Documents/', '/brain/')
                url = join(dname, fname)
                entry = '%s[%s](%s) - %s words\n' % (bullet_indent(indents + 1), fname, url, words)
                result.append(entry)
        return file_words

    def append_directories(d, i):
        for f in sorted(listdir(d)):
            if isdir(join(d, f)):
                dir_index(result, join(d, f), i + 1)

    def dir_index(result, d, i):
        dname = d.split('/')[-1]
        url = d.replace('Documents/', '/brain/')
        result.append('%s[%s](%s)/\n' % (bullet_indent(i), dname, url))
        file_words = append_files(d, i)
        result.append('%s[%s](%s) - %s words/\n' % (bullet_indent(i), dname, url, file_words))

        append_directories(d, i)

        # for fname in sorted(listdir(d)):
        #     if isfile(join(d, fname)):
        #         # url = root + '--' + d + '--' + fname
        #         dname = d.replace('Documents/', '/brain/')
        #         url = join(dname, fname)
        #         result.append('%s[%s](%s)\n' % (bullet_indent(i + 1), fname, url))
        # for f in sorted(listdir(d)):
        #     if isdir(join(d, f)):
        #         dir_index(result, root, join(d, f), i + 1)

    result = []
    d = join('Documents', doc)
    dir_index(result, d, 0)
    return markdown_to_html('\n'.join(result))


# Find the path to the requested document
def doc_path(doc):
    return join('Documents', doc)


# Redirect to an Index for any directory
def doc_redirect(doc):
    while doc.endswith('/'):
        doc = doc[:-1]
    path = doc_path(doc)
    if isdir(path):
        # if exists(join(path, 'Index')) or exists(join(path, 'Index.md')):
            return doc_url(doc + '/Index')
        # return doc_url(doc + '/Directory')
    if not exists(path) and not exists(path + '.md'):
        return doc_url(doc + '/Missing')


# Extract the title from the file text
def doc_title(doc):
    text = read_markdown(doc)
    if text.startswith('#'):
        return text.split('\n')[0][2:]
    else:
        return "** NO DOCUMENT TITLE **"


# Create the URL that corresponds to this document
def doc_url(doc):
    return join('/brain', doc)


# List the file as hyperlinks to documents
def list_files(title):

    def file_entry(path, f):
        if isdir(doc_path(join(path, f))):
            return "%s/" % f
        else:
            if f != '.DS_Store':
                return f

    path = doc_path(title)
    if exists(path) and isdir(path):
        return [file_entry(path, f) for f in sorted(listdir(path))]


# Convert markdown text to HTML
def markdown_to_html(markdown):
    return shell_pipe('pandoc', markdown)


# Return context settings for the views
def page_settings(**kwargs):
    kwargs['header'] = dict(title='My Notes', subtitle=kwargs.get('title'))
    kwargs['time'] = now()
    return kwargs


# Read the specific document
def read_markdown(doc):
    path = doc_path(doc)
    if not exists(path) and exists(path + '.md'):
        path = path + '.md'
    if exists(path) and isfile(path):
        return open(path).read()
    else:
        return 'No DOCUMENT Found, doc=%s, path=%s' % (doc, path)


# Read the document formatted as HTML
# def render_doc(doc):
#     path = doc_path(doc)
#     if not exists(path) and exists(path + '.md'):
#         doc = doc + '.md'
#     return doc_html(doc)


# Run an application and connect with input and output
def shell_pipe(command, stdin=''):
    p = Popen(command, stdin=PIPE, stdout=PIPE)
    if version_info.major == 3:
        (out, error) = p.communicate(input=stdin.encode('utf-8'))
        if error:
            return error.decode('utf-8') + out.decode('utf-8')
        return out.decode('utf-8')
    else:
        (out, error) = p.communicate(input=stdin)
        if error:
            return "**stderr**\n" + error + out
        return out
