from django import template
from django.conf import settings

register = template.Library()

ALLOWABLE_VALUES = ("AWS_S3_CUSTOM_DOMAIN", "DOMAIN",)

# Get settings value on templates
@register.simple_tag
def settings_value(name):
    if name in ALLOWABLE_VALUES:
        return getattr(settings, name, '')
    return ''