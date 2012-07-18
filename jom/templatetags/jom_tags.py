'''
Created on Jul 18, 2012

@author: rax
'''

from django import template
from jom.factory import JomFactory

register = template.Library()
 
@register.inclusion_tag('jom/templatetags/JomInstance.js',
        takes_context = False)
def jom_instance(instance):
    jomEntry = JomFactory.default().getForInstance
    return {'config': jomEntry.renderInstance(instance)}