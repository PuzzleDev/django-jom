{% load jom_tags %}{% for instance in queryset %}
{% register_instance instance %}{% endfor %}