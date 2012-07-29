'''
Copyright PuzzleDev s.n.c.
Created on Jul 24, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from jom.ajax import AjaxResponse
from jom.factory import JomFactory

@AjaxResponse()
def jom_async_save_ajax(request):
    values = request.POST
    factory = JomFactory.default()
    factory.saveJom(values)
    return {}
    