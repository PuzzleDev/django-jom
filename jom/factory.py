'''
Created on Jul 18, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.db import models
from django.template.loader import render_to_string
from django.db.models.fields.files import FileField


class JomFactory(object):
    """ Stores all the JomEntry
    """
    __instance = None
    entries = []
    
    def register(self, entry):
        if entry not in self.entries:
            self.entries.append(entry)
        else:
            raise AssertionError(
                    "JomEntry %s was already registered" % entry) 

    @classmethod
    def default(cls):
        if cls.__instance == None:
            cls.__instance = JomFactory()
        return cls.__instance        
    
    def getForModel(self, model):
        for entry in self.entries:
            if entry.model == model:
                return entry
        raise AssertionError(
                "%s instance is not registered." % model)
    
    def getForInstance(self, instance):
        model = instance.__class__
        return self.getForModel(model)
        

class JomEntry(object):
    """ Converts a Model into a javascript object
    
        For each model that you want to export you should do
        
        FooJomEntry(JomEntry):
            model = Foo
            fields = ['foo', 'bar']
            
        JomFactory.default().register(FooJomEntry)
    """
    model = None
    fields = None
    exclude = None
    template = "jom/JomEntry.js"
    include = None
    
    def __init__(self):
        if self.model == None:
            # model cannot be null
            raise AssertionError(
                    "Model cannot be null.")
        elif not issubclass(self.model, models.Model):
            # model should be a subclass of Model
            raise AssertionError(
                    "Given class %s is not a Model."
                    % self.model)
            
        if self.fields == None:
            self.fields = self.model._meta.fields
        if self.exclude != None:
            self.fields -= self.exclude


    def renderClass(self):
        """ Creates 
        """
        dictionary = {
                'clazz': self.__class__,
                'include': self.include}
        
        fields = [x
            for x in self.model._meta.fields
            if x.name in self.fields]
        
        field_list = []
        for field in fields:
            field_list.append({
                'name': field.name,
                'defaultValue': field.default
                });
        
        dictionary['fields'] = field_list
        return render_to_string(self.template, dictionary)


    def renderInstance(self, instance,
            template = "jom/JomInstance.js"):
        if not isinstance(instance, self.model):
            # model cannot be null
            raise AssertionError(
                    "%s instance is not an instance of %s." %
                    (instance, self.model))
            
        dictionary = {'clazz': self.__class__,}
        field_values = {}
        for field in self.fields:
            field_instance = self.model._meta.fields[field]
            if isinstance(field_instance, FileField):
                if field_instance.name != None:
                    field_values[field] = field_instance.url
                else:
                    field_values[field] = ""
            else:
                field_values[field] = field_instance.value
        dictionary['fields'] = field_values
        
        return render_to_string(template, dictionary)
        
        