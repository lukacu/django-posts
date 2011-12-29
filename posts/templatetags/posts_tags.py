# -*- Mode: python; indent-tabs-mode: nil; c-basic-offset: 2; tab-width: 2 -*-

from django import template
from django.template import Library
from django.template import RequestContext
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.conf import settings
from django.template import Node
from django.utils.encoding import force_unicode
from django.utils.functional import allow_lazy

register = Library()

class TeaserNode(Node):
    def __init__(self, length, more, nodelist):
        self.length = length
        self.more = more
        self.nodelist = nodelist

    def __repr__(self):
        return "<TeaserNode>"

    def render(self, context):
        from django.utils.text import truncate_html_words
        length = self.length.resolve(context)
        context.push()
        original = self.nodelist.render(context)
        output = truncate_html_words(original, length)
        context.pop()

        if len(output) < len(original):
          context.push()
          output = output + self.more.render(context)
          context.pop()
        return output

def do_teaser(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 2:
        raise TemplateSyntaxError("%r expected length" % bits[0])
    length = parser.compile_filter(bits[1])
    nodelist = parser.parse(('more',))
    parser.delete_first_token()
    more = parser.parse(('endteaser',))
    parser.delete_first_token()
    return TeaserNode(length, more, nodelist)
do_teaser = register.tag('teaser', do_teaser)

