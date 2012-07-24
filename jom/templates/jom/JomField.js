/* Get {{ name }} */
{{ clazz }}.prototype.get{{ name|capfirst }} = function() {
	return this.fields['{{ name }}'];
};

{% if not readonly %}/* Set {{ name }} */
{{ clazz }}.prototype.set{{ name|capfirst }} = function(value) {
	this.fields['{{ name }}'] = value;
};
{%endif%}