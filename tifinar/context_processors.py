import os
from django.conf import settings

from .models import msgs

def messages_count(request):
    """عداد الرسائل الجديدة للمستخدم"""
    new_messages_count = 0
    if request.user.is_authenticated:
        # حساب الرسائل التي destinataire هو المستخدم الحالي ولم يتم قراءتها
        new_messages_count = msgs.objects.filter(
            recipient=request.user.id,
            status='unread'  # أو أي حالة تشير إلى "غير مقروءة"
        ).count()
    
    return {'new_messages_count': new_messages_count}

def user_profile_context(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        
        # تحويل المسار إلى صيغة Unix بغض النظر عن نظام التشغيل
        def fix_path(path):
            return path.replace('\\', '/') if path else None
        
        # الحالة الأولى: إذا كان path مخزناً في قاعدة البيانات
        if hasattr(user, 'path') and user.path:
            first_image = user.path.split(',')[0].strip()
            context['user_first_image'] = fix_path(first_image)
        
        # الحالة الثانية: البحث في مجلد static مباشرة
        else:
            user_dir = os.path.join('tifinar', 'images', 'users', str(user.id))
            static_dir = os.path.join(settings.STATICFILES_DIRS[0], user_dir)
            
            if os.path.exists(static_dir):
                for file in os.listdir(static_dir):
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        context['user_first_image'] = fix_path(os.path.join(user_dir, file))
                        break
    
    return context
