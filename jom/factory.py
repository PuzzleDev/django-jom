'''
Created on Jul 18, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.conf import settings
from django.db.models.fields.files import FileField
from django.db import models
from django.template.loader import render_to_string


class JomFactory(object):
    """ Stores all the JomEntry
    """
    __instance = None
    entries = {}
    
    def register(self, entry):
        if not self.entries.has_key(entry.model):
            self.entries[entry.model] = entry
        else:
            raise AssertionError(
                    "JomEntry %s was already registered" % entry) 

    @classmethod
    def default(cls):
        if cls.__instance == None:
            cls.__instance = JomFactory()
        return cls.__instance        
    
    @classmethod
    def autodiscover(cls):
        apps = settings.INSTALLED_APPS
        for app in apps:
            try:
                #import all the JOM classes
                __import__(app + ".joms", globals={},
                        locals={}, fromlist=[], level=-1)
                print("[JOM] Importing: " + app + ".joms")
            except ImportError, ex:
                print("[JOM] Import error: %s " % ex)
    
    def getForModel(self, model):
        jomEntry = self.entries[model]
        if jomEntry:
            return jomEntry()
    
    def getForInstance(self, instance):
        return self.getForModel(instance.__class__)
        

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
                'clazz': self.__class__.__name__,
                'include': self.include}
        
        fields = [x
            for x in self.model._meta.fields
            if x in self.fields]
        
        field_list = []
        for field in fields:
            field_list.append({
                'name': field.name,
                'defaultValue': "null"
                });
        
        dictionary['fields'] = field_list
        return render_to_string(self.template, dictionary = dictionary)


    def instanceToDict(self, instance):
        if not isinstance(instance, self.model):
            # model cannot be null
            raise AssertionError(
                    "%s instance is not an instance of %s." %
                    (instance, self.model))
            
        dictionary = {'clazz': self.__class__.__name__,}
        field_values = {}
        for field in self.fields:
            field_name = field.name
            field_value = getattr(instance, field_name)
            if isinstance(field, FileField):
                if field_value.name != None:
                    field_values[field_name] = field_value.url
            else:
                if field_value:
                    field_values[field_name] = field_value
            # TODO(msama): handle FK and M2M
        dictionary['fields'] = field_values
        
        return dictionary
        
        