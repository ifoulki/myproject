from django import template
from django.conf import settings
import re
import random
register = template.Library()
# custom_filters.py
from django import template
from django.contrib.auth.models import User

register = template.Library()
from django import template

from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def humanize_time(value):
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    
    # إذا كانت الرسالة من اليوم
    if diff.days == 0:
        if diff.seconds < 60:
            return "الآن"
        elif diff.seconds < 3600:
            minutes = diff.seconds // 60
            return f"منذ {minutes} دقيقة"
        else:
            hours = diff.seconds // 3600
            return f"منذ {hours} ساعة"
    
    # إذا كانت الرسالة من الأمس
    elif diff.days == 1:
        return "أمس"
    
    # إذا كانت الرسالة من هذا الأسبوع
    elif diff.days < 7:
        return f"منذ {diff.days} أيام"
    
    # إذا كانت الرسالة من هذا الشهر
    elif diff.days < 30:
        weeks = diff.days // 7
        if weeks == 1:
            return "منذ أسبوع"
        else:
            return f"منذ {weeks} أسابيع"
    
    # إذا كانت الرسالة قديمة
    else:
        months = diff.days // 30
        if months == 1:
            return "منذ شهر"
        elif months < 12:
            return f"منذ {months} أشهر"
        else:
            years = diff.days // 365
            if years == 1:
                return "منذ سنة"
            else:
                return f"منذ {years} سنوات"

@register.filter
def message_date(value):
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    
    # إذا كانت الرسالة من اليوم، نعرض الوقت فقط
    if diff.days == 0:
        return value.strftime("%H:%M")
    
    # إذا كانت الرسالة من الأمس أو هذا الأسبوع
    elif diff.days < 7:
        days_arabic = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
        day_name = days_arabic[value.weekday()]
        return f"{day_name} {value.strftime('%H:%M')}"
    
    # إذا كانت الرسالة قديمة، نعرض التاريخ الكامل
    else:
        return value.strftime("%Y/%m/%d %H:%M")
    
register = template.Library()

@register.filter
def split_string(value, delimiter=','):
    """يقسم السلسلة بناء على محدد معين"""
    if value and isinstance(value, str):
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    return []

@register.filter
def get_user_by_email(email):
    try:
        return User.objects.filter(email=email).first()
    except:
        return None

@register.filter
def get_user_images(email):
    try:
        user = User.objects.filter(email=email).first()
        if user:
            return getattr(user, 'images', '❌ فارغ')
        return '❌ مستخدم غير موجود'
    except:
        return '❌ خطأ'

@register.filter
def get_user_path(email):
    try:
        user = User.objects.filter(email=email).first()
        if user:
            return getattr(user, 'path', '❌ فارغ')
        return '❌ مستخدم غير موجود'
    except:
        return '❌ خطأ'
    
@register.filter
def get_user_by_email(email):
    try:
        return User.objects.filter(email=email).first()
    except:
        return None
    
register = template.Library()

@register.filter
def clean_float(value):
    try:
        num = float(value)
        if num.is_integer():
            return str(int(num))
        else:
            # عرض منزلتين عشريتين فقط إذا كانت هناك حاجة
            return f"{num:.2f}".rstrip('0').rstrip('.')
    except (ValueError, TypeError):
        return str(value)
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

@register.filter
def parse_social_media(value):
    """
    يحول سلسلة وسائل التواصل الاجتماعي إلى قائمة من القواميس
    "facebook:hamid.bialouan, youtube:hamid4TV, instagram:bbc5" 
    -> [{'platform': 'facebook', 'username': 'hamid.bialouan'}, ...]
    """
    if not value:
        return []
    
    social_list = []
    accounts = value.split(',')
    
    for account in accounts:
        account = account.strip()
        if ':' in account:
            platform, username = account.split(':', 1)
            social_list.append({
                'platform': platform.strip().lower(),
                'username': username.strip()
            })
    
    return social_list