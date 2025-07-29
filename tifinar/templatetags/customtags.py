from django import template
from django.template.defaultfilters import stringfilter

from django import template

register = template.Library()

@register.filter
def my_custom_filter(value):
    return value.upper()


register = template.Library()
@register.filter
# @stringfilter

def first_char(value):
    return value[1]

@register.simple_tag
def author(username):
    if username:
        return f"author: {username }"
    else:
        return False


@register.filter
def split(value, key):
    if not value:
        return []
    return [item.strip() for item in value.split(key)]  # strip يزيل الفراغات حول كل جزء