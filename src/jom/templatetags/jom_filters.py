'''
Created on Jul 26, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django import template
from django.template.defaultfilters import capfirst

register = template.Library()

@register.filter()
def capital(value):
    if not isinstance(value, (str, unicode)):
        value = "%s" % value
    return value.capitalize()

@register.filter()
def camel(value):
    if not isinstance(value, (str, unicode)):
        value = "%s" % value
    values = value.split("_")
    return "".join([capfirst(x) for x in values])