from __future__ import absolute_import
#from urlparse import urlparse
from urllib.parse import urlparse
import hashlib
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django import template

from ..models import Account

register = template.Library()

@register.filter
def base_site_url(value):
	parsed = urlparse(value)
	return parsed.netloc

@register.filter
def email_hash(value):
    u = get_object_or_404(Account, username=value)
    a = hashlib.md5(u.email.encode('utf-8')).hexdigest()
    return a

@register.filter
def display_name(value):
	u = get_object_or_404(Account, username=value)
	if u.first_name or u.last_name:
		n = "%s %s" % (u.first_name, u.last_name)
	else:
		n = "%s" % (u.username)
	return n

@register.filter(name='addcss')
def addcss(field, css):
    old_classes = field.field.widget.attrs.get('class', None)
    new_classes = old_classes + ' ' + css if old_classes else css
    return field.as_widget(attrs={"class": new_classes})
