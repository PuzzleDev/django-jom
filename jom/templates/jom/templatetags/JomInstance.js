{% load jom_tags %}
var {{ jsVarName }} = {{ config.clazz }}({{% for key, value in config.fields.items %}
	'{{ key }}': '{{ value }}'{% if not forloop.last %},{% endif %}{% endfor %}});