from urllib.parse import urlparse

from django import template


register = template.Library()
# this filter allows any template to reference an instance’s model name as <instance>|class_name
@register.filter(name="class_name")
def class_name(instance):
    return instance._meta.model.__name__

@register.filter(name="domain_name")
def get_domain(url):
    return urlparse(url).netloc