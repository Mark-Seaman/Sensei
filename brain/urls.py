from django.conf.urls import url

from .views import *


# URL Routes
urlpatterns = [
    url(r'^$',                                  RedirectRoot.as_view()),
    url(r'^(?P<title>[\w/\-.]*)/Files$',        FilesView.as_view()),
    url(r'^(?P<title>[\w/\-.]*)/Index$',        TreeView.as_view()),
    url(r'^(?P<title>[\w/\-.]*)/Directory$',    DirectoryView.as_view()),
    url(r'^(?P<title>[\w/\-.]*)/Missing$',      MissingView.as_view()),
    url(r'^(?P<title>[\w/\-.]*)/Scorecard$',    ScorecardView.as_view()),
    url(r'^(?P<title>[\w/\-.]*)$',              DocView.as_view()),
]
