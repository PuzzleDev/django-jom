'''
Created on Jul 18, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.conf import settings
from django.db import models
from django.db.models.fields import CharField, IntegerField, FloatField,\
    NullBooleanField, DateTimeField, TimeField, AutoField, BooleanField,\
    TextField, DateField
from django.db.models.fields.files import FileField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.template.base import Template
from django.template.context import Context
from django.template.loader import render_to_string
from django.db.models.base import Model


class JomFactory(object):
    """ Stores all the JomEntry
    
        self.descriptors is a model: descriptor dict.
        self.models is a str: model dict.
    """
    __instance = None
    
    def __init__(self):
        super(JomFactory, self).__init__()
        self.descriptors = {}
        self.models = {}
    
    def register(self, descriptor):
        if not self.descriptors.has_key(descriptor.model):
            # Initialize the descriptor and add it to the dictionary
            desc_instance = descriptor()
            self.descriptors[descriptor.model] = desc_instance
            self.models[descriptor.model.__name__]= desc_instance
            return desc_instance
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
    
    def getForName(self, name):
        return self.models.get(name, None)
    
    def getForModel(self, model):
        return self.descriptors.get(model, None)
    
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
    
    def canGet(self, request):
        """ State if the given request has permission to
            get the instance.
            
            Derived classes should override this method
            with their logic. 
        """
        return False
    
    def canUpdate(self, request):
        """ State if the given request has permission to
            update the instance.
            
            Derived classes should override this method
            with their logic. 
        """
        return False
    
    def canCreate(self, request):
        """ State if the given request has permission to
            create the instance.
            
            Derived classes should override this method
            with their logic. 
        """
        return False
    
    def canDelete(self, request):
        """ State if the given request has permission to
            delete the instance.
            
            Derived classes should override this method
            with their logic. 
        """
        return False
    
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
                    for x in model_fields
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
        self.related = {}
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
                self.related[field_name] = field.rel.to
                self.jom_fields[field_name] = jomFields.ForeignKeyJomField
            elif isinstance(field, ManyToManyField):
                # TODO(msama): handle M2M
                self.related[field_name] = field.rel.to
                self.jom_fields[field_name] = jomFields.StringJomField
            elif isinstance(field, (AutoField, IntegerField, FloatField)):
                # Numeral field    
                self.jom_fields[field_name] = jomFields.NumeralJomField
            elif isinstance(field, (DateTimeField, TimeField, DateField)):
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
                'model': self.descriptor.model.__name__
                }
        
        fields = {}
        for name, fieldClazz in self.descriptor.jom_fields.items():
            readonly = True if name in self.descriptor.readonly else False
            from jom.fields import ForeignKeyJomField
            if issubclass(fieldClazz, ForeignKeyJomField):
                related = self.descriptor.related.get(name, None)
                if related:
                    fk_class = self.factory.getForModel(related).__class__.__name__
                else:
                    fk_class = None
                fields[name] = fieldClazz.renderField(
                        clazz, name, 
                        fk_class,
                        readonly)
            else:
                fields[name] = fieldClazz.renderField(clazz, name, readonly)
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
            self.jom_fields[field_name] = field_class(
                        self.instance,
                        field_name,
                        readonly = field_name in self.descriptor.readonly,
                        factory = self.factory
                        )
    
    def instanceToDict(self):
        dictionary = {}
        for field_name in self.descriptor.jom_fields.keys():
            value = getattr(self.instance, field_name)
            if isinstance(value, Model):
                value = value.pk
            # TODO(msama): handle m2m
            dictionary[field_name] = value
        
        return dictionary

    def toJavascript(self):
        dictionary = {
                'clazz': self.descriptor.__class__.__name__,
                'fields': self.jom_fields
                }
        
        t = Template("{{% for key, fieldInstance in fields.items %}\n" +
                     "'{{ key }}': {{ fieldInstance.toJavascript }}{% if not forloop.last %},{% endif %}{% endfor %}}")
        c = Context(dictionary)
        return t.render(c)
    
    def update(self, dictValues):
        for name, jom_field in self.jom_fields.items():
            if not jom_field.readonly:
                if dictValues.has_key(name):
                    jom_field.setValue(dictValues[name])
        self.instance.save()
        