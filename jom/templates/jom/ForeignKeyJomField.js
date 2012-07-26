{% load jom_filters %}/** 
 * Get {{ name }} 
 * 
 * @callback callback(jomInstance)
 */
{{ clazz }}.prototype.get{{ name|camel|capfirst }}Jom = function(callback) {
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

/**
 * Get FK id for field{{ name }}
 *
 * @return the Fk id.
 */
{{ clazz }}.prototype.get{{ name|camel|capfirst }} = function() {
	return this.fields['{{ name }}'];
};

{% if not readonly %}/**
 * Set FK id for {{ name }}.
 * If the factory already contains an instance with the given
 * ID then also the instance is stored as a FK.
 *
 * @param instanceId the FK id.
 */
{{ clazz }}.prototype.set{{ name|camel|capfirst }} = function(instanceId) {
	this.fields['{{ name }}'] = instanceId;
	// Get if it exists
	this.fk['{{ name }}'] = singleton{{ clazz }}Factory.get(instanceId);
};

/**
 * Set {{ name }}
 *
 * @param jomInstance the instance to set.
 */
{{ clazz }}.prototype.set{{ name|camel|capfirst }}Jom = function(jomInstance) {
	if (jomInstance != null) {
		this.fields['{{ name }}'] = jomInstance.getId();
		this.fk['{{ name }}'] = jomInstance;		
	} else {
		this.fields['{{ name }}'] = null;
		this.fk['{{ name }}'] = undefined;	
	}

};{% endif %}