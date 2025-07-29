from django import template

register = template.Library()

@register.filter
def split(value, key):
    """
    يقسم النص إلى قائمة بناءً على الفاصل key
    """
    if value:
        return value.split(key)
    return []
