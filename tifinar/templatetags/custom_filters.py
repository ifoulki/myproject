from django import template

import re

register = template.Library()

@register.filter(name='youtube_url_check')
def youtube_url_check(url):
    """
    Check if a URL is a YouTube URL
    """
    if not url:
        return False
        
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    return re.match(youtube_regex, url) is not None

@register.filter
def split(value, key=','):
    """
    يقسم النص إلى قائمة بناءً على الفاصل (افتراضيًا الفاصلة)
    ويزيل المسافات البيضاء من كل عنصر
    """
    if not value:
        return []
    return [item.strip() for item in value.split(key) if item.strip()]

@register.filter
def trim(value):
    """
    يزيل المسافات البيضاء من بداية ونهاية النص
    """
    return value.strip() if value else value