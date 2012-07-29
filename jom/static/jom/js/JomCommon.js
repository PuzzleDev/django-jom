/**
 * Created on Jul 24, 2012
 * 
 * @author: Michele Sama (m.sama@puzzledev.com)
 * 
 * Common utilities for handling jom instances.
 */

capfirst = function(value) {
	if (value == null || value == undefined) {
		throw "capfirst expects a valid string. Found: " + value + ".";
	}
	if (value.length == 1) {
		return value.toUpperCase();
	}
	return value.charAt(0).toUpperCase() + value.substring(1, value.length);
};

camel = function(value) {
	if (value == null || value == undefined) {
		throw "capfirst expects a valid string. Found: " + value + ".";
	}
	var values = value.split("_");
	var result = "";
	for (var i in values) {
		result = result.concat(capfirst(values[i]));
	}
	return result;
};