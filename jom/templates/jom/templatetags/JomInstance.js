{
{% for key, values in config.fields.items %}
	'{{ key }}': {{ value }}{{ if foorloop.last }},{{ endif }}
{% endfor %}
}