# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*-

from django.contrib.syndication.views import Feed
from django.contrib.markup.templatetags.markup import markdown
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from posts.models import Post

class LatestPostsFeed(Feed):
    title = _("Recent posts")
    description = _("Recent posts")

    def link(self):
      return reverse("posts-archive")

    def items(self):
        return Post.objects.filter(is_public = True).order_by('-date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown(item.text)

