from django.conf.urls import url
from django.contrib.auth.views import login, logout

from mybook_views import BookNotes, MyBookDocDisplay, MyBookPrivateDoc

urlpatterns = [

    # Authentication
    url(r'^login',      login, {'template_name': 'mybook_login.html'}, name='login'),
    url(r'^logout$',    logout, {'next_page': '/login'}),

    # Custom Pages
    url(r'^booknotes/(?P<title>[\w/\-.]*)$',    BookNotes.as_view()),
    # url(r'^inspire',                            SpiritualSelect.as_view()),
    # url(r'^seamanslog/(?P<title>[\w/\-.]*)',    SeamansLog.as_view()),

    # Documents
    url(r'^info/(?P<title>[\w/\-_.]*)$', MyBookPrivateDoc.as_view()),
    url(r'^(?P<title>[\w/\-_.]*)$', MyBookDocDisplay.as_view()),

]
