'''
Created on Jul 18, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.conf import settings
from django.db.models.fields.files import FileField
from django.db import models
from django.template.loader import render_to_string
from django.db.models.fields import CharField, IntegerField, FloatField,\
    NullBooleanField, DateTimeField, TimeField, AutoField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from jom.fields import UrlJomField, StringJomField, BooleanJomField,\
    NumeralJomField, DateJomField
from django.forms.fields import BooleanField
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
        return self.descriptors[model]
    
    def getJomInstance(self, instance):
        return JomInstance(
                self.getForModel(instance.__class__), instance)
        
    def getJomClass(self, model):
        return JomClass(self.getForModel(model))
        

class JomDescriptor(type):
    model = None
    fields = None
    exclude = None
    include = None


class JomEntry(object):
    def __init__(self, descriptor):
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
        
        self.include = descriptor.include
        self.descriptor = descriptor


class JomClass(JomEntry):
    template = "jom/JomEntry.js"
    
    def renderClass(self):
        dictionary = {
                'clazz': self.descriptor.__class__.__name__,
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

    

class JomInstance(JomEntry):
    
    def __init__(self, descriptor, instance):
        super(JomInstance, self).__init__(descriptor)
        if not isinstance(instance, self.__meta__.model):
            # model cannot be null
            raise AssertionError(
                    "%s instance is not an instance of %s." %
                    (instance, self.__meta__.model))
        self.instance = instance
        self.descriptor = descriptor
    
    def toDict(self):
        dictionary = {'clazz': self.descriptor.__class__.__name__,}
        jom_fields = {}
        for field in self.fields:
            field_name = field.name
            field_value = getattr(self.instance, field_name)
            if isinstance(field, FileField):
                # File field
                if field_value.name != None:
                    jom_fields[field_name] =\
                            UrlJomField(field_name, field_value.url)
            elif isinstance(field, (BooleanField, NullBooleanField)):
                # Boolean field
                jom_fields[field_name] =\
                        BooleanJomField(field_name, field_value)
            elif isinstance(field, CharField):
                # Char field
                jom_fields[field_name] =\
                        StringJomField(field_name, field_value)
            elif isinstance(field, ForeignKey):
                # TODO(msama): handle FK and M2M
                jom_fields[field_name] =\
                        StringJomField(field_name, field_value.__str__())
            elif isinstance(field, ManyToManyField):
                # TODO(msama): handle FK and M2M
                jom_fields[field_name] =\
                        StringJomField(field_name, field_value.__str__())
            elif isinstance(field, (AutoField, IntegerField, FloatField)):
                # Numeral field    
                jom_fields[field_name] =\
                        NumeralJomField(field_name, field_value)
            elif isinstance(field, (DateTimeField, TimeField, DateTimeField)):
                # Numeral field
                jom_fields[field_name] =\
                        DateJomField(field_name, field_value)
            else:
                raise ArgumentError("Field not handled.")
            
        dictionary['fields'] = jom_fields
        return dictionary

    
    def toJavascript(self):
        t = Template("new {{ config.clazz }}({{% for key, jomField in config.fields.items %}\n" +
                     "'{{ key }}': {{ jomField.toJavascript }}{% if not forloop.last %},{% endif %}{% endfor %}})")
        c = Context(self.toDict())
        return t.render(c)
        
        return self.value