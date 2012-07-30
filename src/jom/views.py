'''
Copyright PuzzleDev s.n.c.
Created on Jul 24, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from jom.ajax import AjaxResponse
from jom.factory import JomFactory

@AjaxResponse()
def jom_async_save_ajax(request):
    values = request.POST.dict()
    print values
    factory = JomFactory.default()
    model = values.get('model')
    descriptor = factory.getForName(model)
    
    if descriptor == None:
            raise ValueError(
                    "Descriptor for model %s was not registered" % 
                    model)
            
    if not descriptor.canUpdate(request):
        raise ValueError(
                "Permission denied for user %s." %
                request.user)
        
    instance = descriptor.model.objects.get(
            id = values.get("id"))
    
    jomInstance = factory.getJomInstance(instance)
    jomInstance.update(values)
    return {}


@AjaxResponse()
def jom_async_create_ajax(request):
    values = request.POST.dict()
    factory = JomFactory.default()
    model = values.get('model')
    descriptor = factory.getForName(model)
    
    if descriptor == None:
            raise ValueError(
                    "Descriptor for model %s was not registered" % 
                    model)
            
    if not descriptor.canSave(request):
        raise ValueError(
                "Permission denied for user %s." %
                request.user)
        
    instance = descriptor.model()    
    jomInstance = factory.getJomInstance(instance)
    jomInstance.update(values)
    return {}
    
    
@AjaxResponse()
def jom_async_delete_ajax(request):
    values = request.POST.dict()
    factory = JomFactory.default()
    model = values.get('model')
    descriptor = factory.getForName(model)
    
    if descriptor == None:
            raise ValueError(
                    "Descriptor for model %s was not registered" % 
                    model)
            
    if not descriptor.canDelete(request):
        raise ValueError(
                "Permission denied for user %s." %
                request.user)
        
    instance = descriptor.model.objects.get(
            id = values.get("id"))
    
    instance.delete()
    return {}
    
    