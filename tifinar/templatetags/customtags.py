from django import template
from django.template.defaultfilters import stringfilter

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
