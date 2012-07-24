'''
Created on Jul 18, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.conf import settings
from django.db.models.fields.files import FileField
from django.db import models
from django.template.loader import render_to_string
from django.db.models.fields import CharField, IntegerField, FloatField,\
    NullBooleanField, DateTimeField, TimeField, AutoField, BooleanField,\
    TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.template.base import Template
from django.template.context import Context


class JomFactory(object):
    """ Stores all the JomEntry
    """
    __instance = None
    descriptors = {}
    
    def register(self, descriptor):
        if not self.descriptors.has_key(descriptor.model):
            # Initialize the descriptor and add it to the dictionary
            self.descriptors[descriptor.model] = descriptor()
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
    
    """ Which fields have to be read-only.
    """
    readonly = ['id',]
    
    """ A dictionary name: JomFieldclass
        Override this to force the desired JomField
    """
    force_jom_fields = {}
    
    """ The template to be used to create the Jom.
        WARNING: change this only if you know 
        what you are doing!
    """
    template = "jom/JomClass.js"
    
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
            model_fields = self.model._meta.fields
        if self.exclude != None:
            model_fields = [x
                    for x in self.model_fields
                    if x.name not in self.exclude]
        
        if self.template == None:
            raise AssertionError("Template cannot be None.")
        if self.fields == None:
            # Include all model fields
            model_fields = self.model._meta.fields
        else:
            # Include only selected model fields
            model_fields = [x
                    for x in self.model._meta.fields
                    if x.name in self.fields]
        if self.exclude != None:
            # Exclude excluded model fields
            model_fields = [x
                    for x in model_fields
                    if x.name not in self.exclude]
        
        # Init jom_fields
        from jom import fields as jomFields
        self.jom_fields = dict(self.force_jom_fields)
        for field in model_fields:
            field_name = field.name

            # Skip already set fields
            if self.jom_fields.has_key(field_name):
                continue
            elif isinstance(field, FileField):
                self.jom_fields[field_name] = jomFields.UrlJomField
            elif isinstance(field, (BooleanField, NullBooleanField)):
                # Boolean field
                self.jom_fields[field_name] = jomFields.BooleanJomField
            elif isinstance(field, (CharField, TextField)):
                # Char field
                self.jom_fields[field_name] = jomFields.StringJomField
            elif isinstance(field, ForeignKey):
                # FK
                self.jom_fields[field_name] = jomFields.ForeignKeyJomField
            elif isinstance(field, ManyToManyField):
                # TODO(msama): handle M2M
                self.jom_fields[field_name] = jomFields.StringJomField
            elif isinstance(field, (AutoField, IntegerField, FloatField)):
                # Numeral field    
                self.jom_fields[field_name] = jomFields.NumeralJomField
            elif isinstance(field, (DateTimeField, TimeField, DateTimeField)):
                # Numeral field
                self.jom_fields[field_name] = jomFields.DateJomField
            else:
                raise Exception("Field not handled: %s." % field)
            

class JomEntry(object):
    def __init__(self, descriptor, factory = JomFactory.default()):
        if descriptor == None:
            raise AssertionError("Descriptor cannot be None.")
        self.descriptor = descriptor
        self.factory = factory


class JomClass(JomEntry):
    
    def renderClass(self):
        clazz = self.descriptor.__class__.__name__
        dictionary = {
                'clazz': clazz,
                }
        
        fields = {}
        for name, fieldClazz in self.descriptor.jom_fields.items():
            fields[name] = fieldClazz.renderField(clazz, name)
        dictionary['fields'] = fields
        
        return render_to_string(
                self.descriptor.template, dictionary = dictionary)
    

class JomInstance(JomEntry):
    
    def __init__(self, descriptor, instance,
            factory = JomFactory.default()):
        super(JomInstance, self).__init__(descriptor, factory)
        if not isinstance(instance, self.descriptor.model):
            # model cannot be null
            raise AssertionError(
                    "%s instance is not an instance of %s." %
                    (instance, self.descriptor.model))
        self.instance = instance
        self.jom_fields = {}
        for field_name, field_class in self.descriptor.jom_fields.items():
            field_value = getattr(self.instance, field_name)

            self.jom_fields[field_name] = field_class(
                        field_name,
                        field_value,
                        readonly = field_name in self.descriptor.readonly,
                        factory = self.factory
                        )
        
    
    def toDict(self):
        dictionary = {'clazz': self.descriptor.__class__.__name__,
                      'fields': self.jom_fields
                      }
        return dictionary

    
    def toJavascript(self):
        t = Template("{{% for key, fieldInstance in fields.items %}\n" +
                     "'{{ key }}': {{ fieldInstance.toJavascript }}{% if not forloop.last %},{% endif %}{% endfor %}}")
        c = Context(self.toDict())
        return t.render(c)