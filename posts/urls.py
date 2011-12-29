# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*-

from django.conf.urls.defaults import *
from posts.feeds import LatestPostsFeed

urlpatterns = patterns('posts.views',
    url(r'^/?$', 'archive', name="posts-archive"),
    url(r'^recent/?$', 'recent', name="posts-recent"),
    url(r'^(?P<year>[0-9]+)/?$','archiveyear', name="posts-archive-year"),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/?$','archivemonth', name="posts-archive-month"),
    url(r'^(?P<slug>[0-9]+/[0-9]+/[a-z\-_0-9\/]+)/?$','post', name="posts-post"),
    url(r'^feed/?$', LatestPostsFeed(), name="posts-feed"),
)
