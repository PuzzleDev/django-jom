/**
 * Created on Jul 24, 2012
 * 
 * @author: Michele Sama (m.sama@puzzledev.com)
 * 
 * Common utilities for handling jom instances.
 */

// The Async save url
var ASYNC_SAVE_URL = '/jom/save/';


/**
 * Utility to save a jom on server.
 * 
 * @param valueMap an associative array representing the 
 * 		jom instance to save.
 * 
 * @callback successCallback()
 * @callback errorCallback(message)
 */
jomAsyncSave = function(valueMap, successCallback, errorCallback) {
	$.ajax({
    	url: ASYNC_SAVE_URL,
    	data: valueMap,
    	dataType: 'json',
    	type: 'POST',
    	traditional: true,
    	success: function(jsonResponse) { 
    		if (jsonResponse.result == true) {
    			successCallback()
    		} else {
    			errorCallback(jsonResponse.message)
    		}
    	},
    	error: function() { 
    		errorCallback("The server was unreachable.");
    	}
	});
}