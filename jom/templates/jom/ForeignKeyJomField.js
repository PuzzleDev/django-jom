/* Get {{ name }} */
{{ clazz }}.prototype.get{{ name|capfirst }} = function(callback) {
	if (this.fk['{{ name}}'] == undefined) {
		throw "Not implemented yet";
	} else {
		callback(this.fk['{{ name}}']);
	}
};

/* Get FK id for field{{ name }} */
{{ clazz }}.prototype.get{{ name|capfirst }}Id = function() {
	return this.fields['{{ name }}'];
};

{% if not readonly %}/* Set FK id for {{ name }} */
{{ clazz }}.prototype.set{{ name|capfirst }}Id = function(value) {
	this.fields['{{ name }}'] = value;
	this.fk['{{ name }}'] = undefined;
};

/* Set {{ name }}*/
{{ clazz }}.prototype.set{{ name|capfirst }} = function(jomInstance) {
	if (jomInstance != null) {
		this.fields['{{ name }}'] = jomInstance.getId();
		this.fk['{{ name }}'] = jomInstance;		
	} else {
		this.fields['{{ name }}'] = null;
		this.fk['{{ name }}'] = undefined;	
	}

};
{%endif%}