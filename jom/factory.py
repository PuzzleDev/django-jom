'''
Created on Jul 18, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.conf import settings
from django.db.models.fields.files import FileField
from django.db import models
from django.template.loader import render_to_string
from django.db.models.fields import CharField, IntegerField, FloatField,\
    NullBooleanField, DateTimeField, TimeField, AutoField, BooleanField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from numpy.oldnumeric.random_array import ArgumentError
from django.template.base import Template
from django.template.context import Context


class JomFactory(object):
    """ Stores all the JomEntry
    """
    __instance = None
    descriptors = {}
    
    def register(self, descriptor):
        if not self.descriptors.has_key(descriptor.model):
            self.descriptors[descriptor.model] = descriptor
        else:
            raise AssertionError(
                    "JomEntry %s was already registered" % descriptor) 

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
        descriptor = self.descriptors[model]
        if not descriptor:
            raise AssertionError(
                "Model was not registered: %s." % model)
        return descriptor
    
    def getJomInstance(self, instance):
        return JomInstance(
                self.getForModel(instance.__class__), instance)
        
    def getJomClass(self, model):
        return JomClass(self.getForModel(model))
        

class JomDescriptor(object):
    """ Describe a Jom node.
        Developers have to override this class
        with all the models that they want
        to export.
        
        TODO(msama): add read only fields.
    """
    
    """ The model which will be exported as a Jom.
        If you define multiple descriptors for the same
        model you will have multiple Joms. 
    """
    model = None
    
    """ The fields to include in the Jom.
        If None all the fields will be exported.
    """
    fields = None
    
    """ The fields to exclude from the Jom.
        If None all the fields in JomDescriptor.fields 
        will be exported.
    """
    exclude = None
    
    """ The template to be used to create the Jom.
        WARNING: change this only if you know 
        what you are doing!
    """
    template = "jom/JomClass.js"
    


class JomEntry(object):
    def __init__(self, descriptor, factory = JomFactory.default()):
        if descriptor.model == None:
            # model cannot be null
            raise AssertionError(
                    "Model cannot be null.")
        elif not issubclass(descriptor.model, models.Model):
            # model should be a subclass of Model
            raise AssertionError(
                    "Given class %s is not a Model."
                    % descriptor.model)
        self.model = descriptor.model    
            
        if descriptor.fields == None:
            self.fields = self.model._meta.fields
        if descriptor.exclude != None:
            self.fields -= descriptor.exclude
        
        if descriptor.template == None:
            raise AssertionError("Template cannot be None.")
        self.template = descriptor.template
        
        self.descriptor = descriptor
        self.factory = factory


class JomClass(JomEntry):
    
    def renderClass(self):
        dictionary = {
                'clazz': self.descriptor.__name__
                }
        
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

    

class JomInstance(JomEntry):
    
    def __init__(self, descriptor, instance,
            factory = JomFactory.default()):
        super(JomInstance, self).__init__(descriptor, factory)
        if not isinstance(instance, self.model):
            # model cannot be null
            raise AssertionError(
                    "%s instance is not an instance of %s." %
                    (instance, self.model))
        self.instance = instance
        
    
    def toDict(self):
        from jom import fields as jomFields
        dictionary = {'clazz': self.descriptor.__name__,}
        jom_fields = {}
        for field in self.fields:
            field_name = field.name
            field_value = getattr(self.instance, field_name)
            #if not field_value:
            #    continue
            
            if isinstance(field, FileField):
                # File field
                if field_value.name != None:
                    jom_fields[field_name] =\
                            jomFields.UrlJomField(field_name, field_value.url, self.factory)
            elif isinstance(field, (BooleanField, NullBooleanField)):
                # Boolean field
                jom_fields[field_name] =\
                        jomFields.BooleanJomField(field_name, field_value, self.factory)
            elif isinstance(field, CharField):
                # Char field
                jom_fields[field_name] =\
                        jomFields.StringJomField(field_name, field_value, self.factory)
            elif isinstance(field, ForeignKey):
                # FK
                jom_fields[field_name] =\
                        jomFields.ForeignKeyJomField(field_name, field_value, self.factory)
            elif isinstance(field, ManyToManyField):
                # TODO(msama): handle FK and M2M
                jom_fields[field_name] =\
                        jomFields.StringJomField(field_name, field_value.__str__(), self.factory)
            elif isinstance(field, (AutoField, IntegerField, FloatField)):
                # Numeral field    
                jom_fields[field_name] =\
                        jomFields.NumeralJomField(field_name, field_value, self.factory)
            elif isinstance(field, (DateTimeField, TimeField, DateTimeField)):
                # Numeral field
                jom_fields[field_name] =\
                        jomFields.DateJomField(field_name, field_value, self.factory)
            else:
                raise ArgumentError("Field not handled: %s." % field)
            
        dictionary['fields'] = jom_fields
        return dictionary

    
    def toJavascript(self):
        t = Template("{{% for key, jomField in fields.items %}\n" +
                     "'{{ key }}': {{ jomField.toJavascript }}{% if not forloop.last %},{% endif %}{% endfor %}}")
        c = Context(self.toDict())
        return t.render(c)