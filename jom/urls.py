'''
Created on Jul 24, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
from django.conf.urls import patterns, url
from jom.views import jom_async_update_ajax, jom_async_create_ajax,\
    jom_async_delete_ajax

urlpatterns = patterns('',
        url(r'^update/$',
            jom_async_update_ajax, 
            name = "jom_async_update_ajax"),
        url(r'^create/$',
            jom_async_create_ajax, 
            name = "jom_async_create_ajax"),
        url(r'^delete/$',
            jom_async_delete_ajax, 
            name = "jom_async_delete_ajax"),
        )