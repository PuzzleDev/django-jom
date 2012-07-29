'''
Created on Jul 24, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.conf.urls import patterns, url
from jom.views import jom_async_save_ajax

urlpatterns = patterns('',
        url(r'^save/$',
            jom_async_save_ajax, 
            name = "jom_async_save_ajax"),)