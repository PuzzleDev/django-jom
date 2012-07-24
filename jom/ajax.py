'''
Copyright PuzzleDev s.n.c.
Created on Jul 24, 2012

@author: Michele Sama (m.sama@puzzledev.com)
'''
import json
from django.http import HttpResponse
import datetime

    

def parseDateTime(date_string):
    try:
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    except:
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    return date

#----------------
RESULT = "result"
MESSAGE = "message"

def json_message(dictionary):
    return json.dumps(dictionary)

def json_response(result, dictionary = {}, message = None):
    dictionary[RESULT] = result
    if message:
        dictionary[MESSAGE] = message
    return json_message(dictionary)

def json_true(dictionary = {}, message = None):
    return json_response(True, dictionary, message)

def json_false(dictionary = {}, message = None):
    return json_response(False, dictionary, message)

class AjaxResponse(object):
    """ Creates an ajax response
    """ 
    
    def __call__(self, original_fz):
        def _decorated_fz(request, *args, **kwargs):         
            if request.method == 'GET':
                return HttpResponse(json_false(message = "Request should be a POST"),
                        content_type = "application/json") 
            
            try:
                dictionary = original_fz(request, *args, **kwargs)
                return HttpResponse(json_true(dictionary = dictionary),
                        content_type = "application/json") 
            except Exception, err:
                return HttpResponse(json_false(message = "%s" % err),
                        content_type = "application/json") 
        return _decorated_fz
    
    