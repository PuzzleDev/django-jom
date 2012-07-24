'''
Created on Jul 19, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
import datetime
from django.template.defaultfilters import safe
from django.db.models.base import Model
from jom import factory as jom_factory
from django.template.loader import render_to_string

class JomField(object):
    """ Define the base class for a field.
    """
    
    def __init__(self, instance, name, readonly = False,
                 factory = jom_factory.JomFactory.default()):
        self.name = name
        self.instance = instance
        self.readonly = readonly
        self.factory = factory

    def getValue(self):
        return getattr(self.instance, self.name)
    
    def setValue(self, value):
        setattr(self.instance, self.name, value)
        
    value = property(getValue, setValue)

    def toString(self):
        raise AssertionError(
                "JomField is abstract")
    
    def toJavascript(self):
        raise AssertionError(
                "JomField is abstract")
        
    @classmethod
    def renderField(self, clazz, name, readonly = False):
        dictionary = {
                'clazz': clazz,
                'name': name,
                'readonly': readonly
                }
        
        return render_to_string(
                'jom/JomField.js', dictionary = dictionary)


class BooleanJomField(JomField):
    """ Define a field wrapping a boolean.
    """
    
    def __init__(self, instance, name, readonly = False,
            factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, bool):
            raise AssertionError(
                "Value should be a boolean. Found: %s." % value)
        super(BooleanJomField, self).__init__(instance, name, readonly, factory)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        return "true" if self.value else "false"
  
        
class NumeralJomField(JomField):
    """ Define a field wrapping a numeral.
    """
    
    def __init__(self, instance, name, readonly = False,
                 factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, (int, long, float)):
            raise AssertionError(
                "Value should be a number. Found: %s." % value)
        super(NumeralJomField, self).__init__(instance, name, readonly, factory)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        # marked safe to avoid comma separators
        return safe(self.value)


class StringJomField(JomField):
    """ Define a field wrapping a string.
    """
    
    def __init__(self, instance, name, readonly = False,
            factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, (str, unicode)):
            value = getattr(instance, name)
            raise AssertionError(
                "Value should be a string. Found: %s." % value)
        super(StringJomField, self).__init__(instance, name, readonly, factory)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        # TODO(msama): handle tabs and new lines
        return safe("\"%s\"" % self.value.replace("\"", "\\\""))
    

class JavascriptJomField(JomField):
    """ Define a field wrapping a string.
    """
    
    def __init__(self, instance, name, readonly = False,
            factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, (str, unicode)):
            raise AssertionError(
                "Value should be a string. Found: %s." % value)
        super(StringJomField, self).__init__(instance, name, readonly, factory)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        return self.value
    

class UrlJomField(JomField):
    """ Define a field wrapping a file.
    """
    def __init__(self, instance, name, readonly = False,
                 factory = jom_factory.JomFactory.default()):
        # TODO(msama): typechecking
        super(UrlJomField, self).__init__(instance, name, readonly, factory)
        
    def getValue(self):
        filefield = getattr(self.instance, self.name)
        if filefield.name != None:
            return filefield.url
        else:
            return ""
    
    def setValue(self, value):
        filefield = getattr(self.instance, self.name)
        filefield.name = value
        
    value = property(getValue, setValue)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        # TODO(msama): handle tabs and new lines
        return safe("\"%s\"" % self.value)


class DateJomField(JomField):
    """ Define a field wrapping a boolean.
    """
    
    def __init__(self, instance, name, readonly = False,
            factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, (datetime.date.Date, 
                datetime.time.Time, datetime.datetime.DateTime)):
            raise AssertionError(
                "Value should be a datetime. Found: %s." % value)
        super(DateJomField, self).__init__(instance, name, readonly, factory)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        return self.value
    

class ForeignKeyJomField(JomField):
    def __init__(self, instance, name, readonly = False,
            factory = jom_factory.JomFactory.default()):
        value = getattr(instance, name)
        if not isinstance(value, Model):
            raise AssertionError(
                "Value should be a Model. Found: %s." % value)
        super(ForeignKeyJomField, self).__init__(instance, name, readonly, factory)
    
    def getValue(self):
        return getattr(self.instance, self.name)
    
    def setValue(self, value):
        if isinstance(value, Model):
            setattr(self.instance, self.name, value)
        elif isinstance(value, dict):
            jomInstance = self.factory.update(value)
            setattr(self.instance, self.name, jomInstance.instance)
        else:
            raise AttributeError(
                    "%s should be a instance of Model or a dict." % value)
            
    value = property(getValue, setValue)
    
    def toString(self):
        return self.value.__srt__()
    
    def toJavascript(self):
        return self.value.id

    @classmethod
    def renderField(self, clazz, name, readonly = False):
        dictionary = {
                'clazz': clazz,
                'name': name,
                'readonly': readonly
                }
        
        return render_to_string(
                'jom/ForeignKeyJomField.js', dictionary = dictionary)