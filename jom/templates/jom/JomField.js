{% load jom_filters %}/* Get {{ name }} */
{{ clazz }}.prototype.get{{ name|camel|capfirst }} = function() {
	return this.fields['{{ name }}'];
};

{% if not readonly %}/* Set {{ name }} */
{{ clazz }}.prototype.set{{ name|camel|capfirst }} = function(value) {
	this.fields['{{ name }}'] = value;
};
{%endif%}