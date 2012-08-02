'''
Created on Jul 18, 2012

@author: rax
'''

from django import template
from jom.factory import JomFactory

register = template.Library()
    
@register.inclusion_tag('jom/templatetags/JomDict.js',
        takes_context = False)
def jom_dict(instance):
    """ Creates an associative array which can
        initialize a JomInstance.
    """
    jomInstance = JomFactory.default().getJomInstance(instance)
    if not jomInstance:
        raise AssertionError(
                "Model not registered: %s" % instance.__class__)
    return {'jomInstance': jomInstance}


@register.inclusion_tag('jom/templatetags/register_instance.js',
        takes_context = False)
def register_instance(instance):
    """ Creates an associative array which can
        initialize a JomInstance.
    """
    jomInstance = JomFactory.default().getJomInstance(instance)
    if not jomInstance:
        raise AssertionError(
                "Model not registered: %s" % instance.__class__)
    return {'jomInstance': jomInstance,
            'clazz': jomInstance.descriptor.__class__.__name__,
            'instance': instance}


@register.inclusion_tag('jom/templatetags/register_queryset.js',
        takes_context = False)
def register_queryset(queryset):
    """ Creates an associative array which can
        initialize a JomInstance.
    """
    return {'queryset': queryset}