from django import template
from django.conf import settings
import re
import random

register = template.Library()

# فلتر get_item
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# فلتر string_to_dict
@register.filter
def string_to_dict(value):
    """يحول سلسلة نصية من الشكل key1:value1,key2:value2 إلى قاموس"""
    result = {}
    for pair in value.split(','):
        if ':' in pair:
            k, v = pair.split(':', 1)
            result[k.strip()] = v.strip()
    return result

# فلتر shuffle
@register.filter(name='shuffle')
def shuffle_filter(value):
    """يخلط العناصر في قائمة"""
    if not value:
        return []
    try:
        if isinstance(value, str):
            value = value.split(',')
        shuffled = list(value)
        random.shuffle(shuffled)
        return shuffled
    except Exception:
        return value

# فلتر split
@register.filter
def split(value, key=','):
    """
    يقسم النص إلى قائمة بناءً على الفاصل (افتراضيًا الفاصلة)
    ويزيل المسافات البيضاء من كل عنصر
    """
    if not value:
        return []
    return [item.strip() for item in value.split(key) if item.strip()]

# فلتر trim
@register.filter
def trim(value):
    """
    يزيل المسافات البيضاء من بداية ونهاية النص
    """
    return value.strip() if value else value

# فلتر youtube_url_check
@register.filter(name='youtube_url_check')
def youtube_url_check(url):
    """يتحقق إذا كان الرابط من YouTube"""
    if not url:
        return False
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return re.match(youtube_regex, url) is not None

# فلتر media_url
@register.filter(name='media_url')
def media_url(path):
    """يحوله إلى رابط كامل داخل MEDIA_URL"""
    if not path:
        return ''
    return f"{settings.MEDIA_URL}{path}"
