/* Get {{ name }} */
{{ clazz }}.prototype.get{{ name|capfirst }} = function(callback) {
	if (this.fk['{{ name}}'] == undefined) {
		var self = this;
		singleton{{ clazz }}Factory.asynchGet(
				this.fields['{{ name }}'],
				// Success callback
				function (jomFk) {
					self.fk['{{ name}}'] = jomFk;
				},
				// Failure callback
				function(msg) {
					console.log(msg)
				});
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

};{% endif %}