'''
Created on Jul 19, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
import datetime
from django.template.defaultfilters import safe
from django.db.models.base import Model
from jom import factory as jom_factory

class JomField(object):
    """ Define the base class for a field.
    """
    
    def __init__(self, name, value, factory = jom_factory.JomFactory.default()):
        self.name = name
        self.value = value
        self.factory = factory
        
    def toString(self):
        raise AssertionError(
                "JomField is abstract")
    
    def toJavascript(self):
        raise AssertionError(
                "JomField is abstract")


class BooleanJomField(JomField):
    """ Define a field wrapping a boolean.
    """
    
    def __init__(self, name, value, factory = jom_factory.JomFactory.default()):
        if not isinstance(value, bool):
            raise AssertionError(
                "Value should be a boolean. Found: %s." % value)
        super(BooleanJomField, self).__init__(name, value, factory)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        return "true" if self.value else "false"
  
        
class NumeralJomField(JomField):
    """ Define a field wrapping a numeral.
    """
    
    def __init__(self, name, value, factory = jom_factory.JomFactory.default()):
        if not isinstance(value, (int, long, float, complex)):
            raise AssertionError(
                "Value should be a number. Found: %s." % value)
        super(NumeralJomField, self).__init__(name, value, factory)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        return self.value


class StringJomField(JomField):
    """ Define a field wrapping a string.
    """
    
    def __init__(self, name, value, factory = jom_factory.JomFactory.default()):
        if not isinstance(value, (str, unicode)):
            raise AssertionError(
                "Value should be a string. Found: %s." % value)
        super(StringJomField, self).__init__(name, value, factory)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        # TODO(msama): handle tabs and new lines
        return safe("\"%s\"" % self.value.replace("\"", "\\"))
    

class UrlJomField(StringJomField):
    """ Define a field wrapping a file.
    """
    pass


class DateJomField(JomField):
    """ Define a field wrapping a boolean.
    """
    
    def __init__(self, name, value, factory = jom_factory.JomFactory.default()):
        if not isinstance(value, (datetime.date.Date, 
                datetime.time.Time, datetime.datetime.DateTime)):
            raise AssertionError(
                "Value should be a datetime. Found: %s." % value)
        super(DateJomField, self).__init__(name, value, factory)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        return self.value
    

class ForeignKeyJomField(JomField):
    def __init__(self, name, value, factory = jom_factory.JomFactory.default()):
        if not isinstance(value, Model):
            raise AssertionError(
                "Value should be a Model. Found: %s." % value)
        super(ForeignKeyJomField, self).__init__(name, value, factory)
        
    def toString(self):
        return self.value.__srt__()
    
    def toJavascript(self):
        if self.factory.descriptors.has_key(self.value.__class__):
            return self.factory.getJomInstance(self.value).toJavascript()
        else:
            return safe("\"%s\"" % self.value)
