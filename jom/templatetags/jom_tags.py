'''
Created on Jul 18, 2012

@author: rax
'''

from django import template
from jom.factory import JomFactory

register = template.Library()
 
@register.inclusion_tag('jom/templatetags/JomInstance.js',
        takes_context = False)
def jom_instance(instance, jsVarName):
    """ Creates a javascript representation of the
        given model instance and saves it in a 
        javascript variable with the given jsVarName
    """
    
    jomInstance = JomFactory.default().getJomInstance(instance)
    if not jomInstance:
        raise AssertionError(
                "Model not registered: %s" % instance.__class__)
    #print(jomInstance.toJavascript())
    return {'jsVarName': jsVarName,
            'jomInstance': jomInstance}