#!/usr/bin/python
# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*-

from datetime import datetime
from inspect import isclass

import django
from django.db import models
from django.db.models.signals import post_init
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str, force_unicode
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField

class Post(models.Model):
    title = models.CharField(_('title'), max_length=200)
    title_slug = models.SlugField(_('title slug'), unique=True, editable = False, max_length=255)
    date = models.DateTimeField(_('date added'), default=datetime.now, editable = False, auto_now_add=True)
    modified = models.DateTimeField(_('date modified'), editable = False, auto_now = True, default=datetime.now)
    text = models.TextField(_('text'), blank=True)
    is_public = models.BooleanField(_('is public'), default=True, help_text=_('Public entries will be displayed in the default views.'))
    tags = TagField(help_text=_('Separate tags with spaces, put quotes around multiple-word tags.'), verbose_name=_('tags'))

    enable_comments = models.BooleanField(_('can comment'), default=True)

    def save(self, *args, **kwargs):
      for i in xrange(0, 1000):
        try:
          if i == 0:
            self.title_slug = "%04d/%02d/%s" % (self.date.year, self.date.month, slugify(self.title))
          else:
            self.title_slug = "%04d/%02d/%s-%i" % (self.date.year, self.date.month, slugify(self.title), i)
          if hasattr(self, "_slug"):
            self._slug == None
          super(Post, self).save(*args, **kwargs)
        except django.db.utils.IntegrityError, e:
          continue
        break

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
      return reverse("posts-post", kwargs={"slug" : self.title_slug })

