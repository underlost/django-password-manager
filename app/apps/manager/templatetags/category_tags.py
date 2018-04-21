from __future__ import absolute_import
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django import template

from coreExtend.models import Account
from manager.models import Category

register = template.Library()

@register.inclusion_tag('manager/templatetags/render_category_list.html', takes_context=True)
def render_categories(context):
    request = context['request']
    categories = Category.objects.all()
    return { 'object_list': categories }
