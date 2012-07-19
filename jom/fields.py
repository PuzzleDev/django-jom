'''
Created on Jul 19, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
import datetime
from django.template.defaultfilters import safe
from django.db.models.base import Model

class JomField(object):
    """ Define the base class for a field.
    """
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def toString(self):
        raise AssertionError(
                "JomField is abstract")
    
    def toJavascript(self):
        raise AssertionError(
                "JomField is abstract")


class BooleanJomField(JomField):
    """ Define a field wrapping a boolean.
    """
    
    def __init__(self, name, value):
        if not isinstance(value, bool):
            raise AssertionError(
                "Value should be a boolean. Found: %s." % value)
        super(BooleanJomField, self).__init__(name, value)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        return self.value
  
        
class NumeralJomField(JomField):
    """ Define a field wrapping a numeral.
    """
    
    def __init__(self, name, value):
        if not isinstance(value, (int, long, float, complex)):
            raise AssertionError(
                "Value should be a number. Found: %s." % value)
        super(NumeralJomField, self).__init__(name, value)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        return self.value


class StringJomField(JomField):
    """ Define a field wrapping a string.
    """
    
    def __init__(self, name, value):
        if not isinstance(value, (str, unicode)):
            raise AssertionError(
                "Value should be a string. Found: %s." % value)
        super(StringJomField, self).__init__(name, value)
        
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
    
    def __init__(self, name, value):
        if not isinstance(value, (datetime.date.Date, 
                datetime.time.Time, datetime.datetime.DateTime)):
            raise AssertionError(
                "Value should be a datetime. Found: %s." % value)
        super(DateJomField, self).__init__(name, value)
        
    def toString(self):
        return self.value
    
    def toJavascript(self):
        return self.value
    

class ForeignKeyJomField(JomField):
    def __init__(self, name, value):
        if not isinstance(value, Model):
            raise AssertionError(
                "Value should be a Model. Found: %s." % value)
        super(DateJomField, self).__init__(name, value)
        
    def toString(self):
        return self.value.__srt__()
    
    def toJavascript(self):
        return self.value.toJavascript()