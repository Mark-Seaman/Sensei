from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.views.generic import RedirectView, TemplateView
from os import listdir
from os.path import join
from random import choice

from tool.document import doc_file_index, doc_html_text, doc_list, doc_page, domain_doc
from tool.log import log, log_page

from .mybook import booknotes_excerpt, get_menu, header_info, theme, seamanslog_settings


class DocDisplay(TemplateView):

    def get_template_names(self):
        theme_template = theme(self.request.get_host())
        # log('theme = %s' % theme_template)
        return [theme_template]

    def get_settings(self):
        title = self.kwargs.get('title', 'Index')
        log_page(self.request)
        text = doc_html_text(title, '/static/images')
        menu = get_menu(title)
        url = self.request.get_raw_uri()
        header = header_info(self.request.get_host())
        return dict(title=title, text=text, menu=menu, url=url, header=header, time=now())

    def get_context_data(self, **kwargs):
        log_page(self.request)
        return self.get_settings()

    def get(self, request, *args, **kwargs):
        title = self.kwargs.get('title', 'Index')

        # Wrong Domain Document
        # domdoc = domain_doc(self.request.get_host(), title)
        # if title != domdoc:
        #     log('REDIRECT DOMAIN: %s --> %s' % (title, domdoc))
        #     return HttpResponseRedirect('/Index')

        # Index or Directory or .md
        url = doc_page(title)
        if url:
            log('REDIRECT: %s --> %s' % (title, url))
            return HttpResponseRedirect('/' + url)

        return self.render_to_response(self.get_context_data(**kwargs))


class DocFileIndex(TemplateView):
    template_name = 'mybook_list.html'

    def get_context_data(self, **kwargs):
        title = self.kwargs.get('title')
        log_page(self.request, title)
        doclist = doc_file_index(title)
        menu = get_menu (title)
        return dict(title=title, list=doclist, menu=menu, url=self.request.get_raw_uri(), header=header_info(self.request.get_host()))


class DocList(TemplateView):
    template_name = 'mybook_list.html'

    def get_context_data(self, **kwargs):
        title = self.kwargs.get('title')
        log_page(self.request, title)
        doclist = doc_list(title)
        menu = get_menu (title)
        return dict(title=title, list=doclist, menu=menu, url=self.request.get_raw_uri(), header=header_info(self.request.get_host()))



class DocMissing(TemplateView):
    template_name = 'mybook_missing.html'

    def get_context_data(self, **kwargs):
        title = self.kwargs.get('title', 'Index')
        menu = get_menu(title)
        header = header_info(self.request.get_host())
        return dict(title=title, menu=menu, header=header, time=now())


class DocRandom(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        title = self.kwargs.get('title')
        files = listdir(join('Documents', title))
        file = choice(files)
        return '/%s/%s' % (title, file)


class DocRoot(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        log_page(self.request, 'Redirect Index')
        return '/%s' % domain_doc(self.request.get_host(),'Index')


class PrivateDoc(LoginRequiredMixin, DocDisplay):

    def get_context_data(self, **kwargs):
        title = self.kwargs.get('title', 'Index')
        domdoc = domain_doc(self.request.get_host(), title)
        text = doc_html_text(domdoc, '/static/images')
        menu = get_menu('info/'+title)
        return dict(title=title, text=text, menu=menu, header=header_info(self.request.get_host()), time=now())

# --------------------------------------

class BookNotes(DocDisplay):
    template_name = 'mybook_theme.html'

    def get_context_data(self, **kwargs):
        title = join('booknotes', self.kwargs.get('title', 'Index'))
        photo = 'MarkSeaman.100.png'
        excerpt, url = booknotes_excerpt(self.kwargs.get('title'))
        kwargs = dict(title=title, photo=photo, text=excerpt, readmore=(url, url), excerpt=excerpt)
        return super(BookNotes, self).get_context_data(**kwargs)


class DailyTask(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        path = 'Documents/info/daily'
        return '/info/daily/%s' % choice(listdir(path))


# class SeamansLog(RedirectView):
#     permanent = False
#     url = '/seamanslog/Random'

class SeamansLog(DocDisplay):

    def get_settings(self):
        title = self.kwargs.get('title', 'Index')
        return seamanslog_settings(self.request.get_host(), title)

    def get_template_names(self):
        return ['seaman_theme.html']



