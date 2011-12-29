#!/usr/bin/python
# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*-

from django.contrib import admin
from attachments.admin import AttachmentInlines

from tagging.forms import TagField
from posts.models import Post
#from hype.widgets import TagAutocomplete

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_public', 'date')
    list_filter = ['is_public']
    inlines = [AttachmentInlines]
#    formfield_overrides = {
#        TagField: {'widget': TagAutocomplete},
#    }



admin.site.register(Post, PostAdmin)
