# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*- 
from datetime import datetime

from django.db.models import Count
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import Http404
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from posts.models import Post

if settings.DATABASES['default']['ENGINE'].find('postgresql') != -1:
  DB_TYPE = "postgresql"
elif settings.DATABASES['default']['ENGINE'].find('mysql') != -1:
  DB_TYPE = "mysql"
elif settings.DATABASES['default']['ENGINE'].find('sqlite') != -1:
  DB_TYPE = "sqlite"

def recent(request):
  if hasattr(request, 'breadcrumbs'):
    request.breadcrumbs(_("Posts"), reverse("posts-archive"))
    request.breadcrumbs(_("Recent"), reverse("posts-recent"))

  return render_to_response('posts/recent.html',
    { "posts" : Post.objects.filter(is_public=True).order_by("-date")[0:5] },
    context_instance = RequestContext(request)
  )

def archive(request):

  if hasattr(request, 'breadcrumbs'):
    request.breadcrumbs(_("Posts"), reverse("posts-archive"))

  if DB_TYPE == "sqlite":
    year = "django_date_trunc('year', 'posts_post'.'date')"
  elif DB_TYPE == "mysql":
    year = "YEAR(`posts_post`.`date`)"

  yearsraw = list(Post.objects.filter(is_public=True).extra(select={"year" : year}).values('year').order_by().annotate(entries=Count('id')))

  if DB_TYPE == "sqlite":
    years = [ {'entries' : o['entries'], 'year' : o['year'][:4]} for o in yearsraw ]
  elif DB_TYPE == "mysql":
    years = [ {'entries' : o['entries'], 'year' : o['year']} for o in yearsraw ]

  return render_to_response('posts/archive.html',
    { "years" : years },
    context_instance = RequestContext(request)
  )

def archiveyear(request, year):
  year = min(int(year), 9999)

  if hasattr(request, 'breadcrumbs'):
    request.breadcrumbs(_("Posts"), reverse("posts-archive"))
    request.breadcrumbs(year, reverse("posts-archive-year", kwargs={"year" : "%04d" % year}))

  if DB_TYPE == "sqlite":
    month = "django_date_trunc('month', 'posts_post'.'date')"
  elif DB_TYPE == "mysql":
    month = "MONTH(`posts_post`.`date`)"
  
  months = [ {'entries' : 0, 'month' : i, 'name' : datetime(2000, i, 1).strftime("%B")} for i in xrange(1, 13) ]

  monthsraw = list(Post.objects.filter(is_public=True, date__year = year).extra(select={"month" : month}).values('month').order_by().annotate(entries=Count('id')))

  if DB_TYPE == "sqlite":
    for o in monthsraw:
      months[int(o['month'][5:7])-1]['entries'] = o['entries']
  if DB_TYPE == "mysql":
    for o in monthsraw:
      months[o['month']-1]['entries'] = o['entries']

  #months = [ {'entries' : o['entries'], 'month' : o['month'][5:7], 'name' : datetime(2000, int(o['month'][5:7]), 1).strftime("%B")} for o in monthsraw ]

  return render_to_response('posts/archive_year.html',
    { "months" : months, "year" : year },
    context_instance = RequestContext(request)
  )

def archivemonth(request, year, month):
  year = min(int(year), 9999)
  month = max(min(int(month), 12), 1)

  if hasattr(request, 'breadcrumbs'):
    request.breadcrumbs(_("Posts"), reverse("posts-archive"))
    request.breadcrumbs(year, reverse("posts-archive-year", kwargs={"year" : "%04d" % year}))
    request.breadcrumbs(datetime(2000, month, 1).strftime("%B"), reverse("posts-archive-month", kwargs={"year" : "%04d" % year, "month" : "%02d" % month}))

  return render_to_response('posts/archive_month.html',
    { "posts" : Post.objects.filter(is_public=True, date__year = year, date__month = month).order_by("-date"), "year" : year, "month" : datetime(2000, month, 1).strftime("%B") },
    context_instance = RequestContext(request)
  )

def post(request, slug):

  try:
    post = Post.objects.get(is_public = True, title_slug=slug)

    if hasattr(request, 'breadcrumbs'):
      request.breadcrumbs(_("Posts"), reverse("posts-archive"))
      request.breadcrumbs(post.date.strftime("%Y"), reverse("posts-archive-year", kwargs={"year" : "%04d" % post.date.year}))
      request.breadcrumbs(post.date.strftime("%B"), reverse("posts-archive-month", kwargs={"year" : "%04d" % post.date.year, "month" : "%02d" % post.date.month}))
      request.breadcrumbs(post.title, reverse("posts-post", kwargs={"slug" : post.title_slug}))

    try:
      previous = Post.objects.filter(is_public = True, date__lt=post.date).order_by("-date")[0]
    except IndexError:
      previous = None

    try:
      next = Post.objects.filter(is_public = True, date__gt=post.date).order_by("date")[0]
    except IndexError:
      next = None

    return render_to_response('posts/post.html',
      {"post" : post, "next" : next, "previous" : previous },
      context_instance = RequestContext(request)
    )
  except Post.DoesNotExist:
      raise Http404


