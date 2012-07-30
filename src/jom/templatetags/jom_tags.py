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
    print(jomInstance.toJavascript())
    return {'jomInstance': jomInstance}
