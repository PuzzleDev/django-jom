'''
Created on Jul 30, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.db import models

class SimpleModel(models.Model):
    """ A simple model with a single field.
    """
    name = models.CharField(max_length = 100)
    

class ModelWithAllFields(models.Model):
    """ A model containing any kind of field with
        the exclusion of related fields
    """
     
    slug = models.SlugField(max_length = 100)
    text = models.TextField(max_length = 100)
    char = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    url = models.URLField(max_length = 100)
    
    integer = models.IntegerField()
    positive_integer = models.PositiveIntegerField()
    small_integer = models.SmallIntegerField()
    small_positive_integer = models.PositiveSmallIntegerField()
    big_integer = models.BigIntegerField()
    float = models.FloatField()
    boolean = models.BooleanField()
    
    comma_separated_integer = models.CommaSeparatedIntegerField(max_length = 100)
    date = models.DateField()
    time = models.TimeField()
    datetime = models.DateTimeField()
    
    file = models.FileField(upload_to = "files/")
    image = models.ImageField(upload_to = "images/")
    
    # This field should be excluded
    excluded_field = models.SlugField(max_length = 100)


class ModelWithOneToOne(models.Model):
    simple = models.OneToOneField(
            SimpleModel,
            related_name = "modelwithonetoone")

class ModelWithFK(models.Model):
    simple = models.ForeignKey(
            SimpleModel,
            related_name = "modelwithfks")


class ModelWithM2M(models.Model):
    simples = models.ManyToManyField(
            SimpleModel,
            related_name = "modelwithm2ms")