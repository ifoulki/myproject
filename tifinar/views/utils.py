from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import FileResponse, Http404
from django.conf import settings
import os
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)

# أدوات التقسيم الصفحي
def paginate_queryset(request, queryset, per_page=10):
    """
    تقسيم النتائج إلى صفحات
    """
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

# معالجة الملفات
def serve_file(file_path, content_type):
    """
    خدمة الملفات المحمية (PDF/صور/إلخ)
    """
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type=content_type)
    raise Http404("File not found")

def serve_pdf(filename):
    """
    خدمة ملفات PDF من مجلد محدد
    """
    decoded_filename = unquote(filename)
    file_path = os.path.join(settings.MEDIA_ROOT, 'ebooks', decoded_filename)
    return serve_file(file_path, 'application/pdf')

# أدوات الأمان
def sanitize_filename(filename):
    """
    تنظيف أسماء الملفات من الأحرف الخطرة
    """
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

# أدوات التسجيل
def log_api_request(request):
    """
    تسجيل طلبات API
    """
    logger.info(
        f"API Request: {request.method} {request.path}",
        extra={
            'user': request.user.username if request.user.is_authenticated else 'anonymous',
            'ip': request.META.get('REMOTE_ADDR')
        }
    )

# أدوات التنسيق
def format_ar_date(dt):
    """
    تنسيق التاريخ بالعربية
    """
    months_ar = [
        "يناير", "فبراير", "مارس", "أبريل",
        "مايو", "يونيو", "يوليو", "أغسطس",
        "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
    ]
    return f"{dt.day} {months_ar[dt.month-1]} {dt.year}"

# أدوات الألعاب (مثال)
def rps_game_logic(user_choice):
    """
    منطق لعبة حجر-ورقة-مقص
    """
    import random
    choices = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(choices)
    
    if user_choice == computer_choice:
        return {'result': 'draw', 'computer_choice': computer_choice}
    
    win_conditions = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }
    
    if win_conditions[user_choice] == computer_choice:
        return {'result': 'win', 'computer_choice': computer_choice}
    else:
        return {'result': 'lose', 'computer_choice': computer_choice}