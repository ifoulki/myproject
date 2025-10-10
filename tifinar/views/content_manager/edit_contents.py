from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from tifinar.models import articles, comments
from tifinar.myForms.article.create_article_form import ArticleForm
from tifinar.forms import CommentForm
from django.contrib import messages
import os
from django.conf import settings
import logging
logger = logging.getLogger(__name__)
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib as mpl
from django.utils import timezone
import unicodedata
import re
from django.utils.text import slugify


plt.rcParams['font.family'] = 'Arial'
mpl.rcParams['axes.unicode_minus'] = False


def reshape_arabic(text):
    """دالة لإعادة تشكيل النصوص العربية"""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)


def generate_chart_image(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100, transparent=True)
    plt.close(fig)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')


def generate_unique_slug(model_class, title, instance=None):
    """إنشاء slug فريد من العنوان"""
    # تنظيف العنوان وإنشاء slug أساسي
    clean = re.sub(r'[^\w\s-]', '', title)
    clean = clean.replace(' ', '_')
    base_slug = slugify(clean, allow_unicode=True)
    
    slug = base_slug
    counter = 1
    
    # إذا كان هناك instance (تحديث)، استثنيه من البحث
    if instance and hasattr(instance, 'pk') and instance.pk:
        queryset = model_class.objects.exclude(pk=instance.pk)
    else:
        queryset = model_class.objects.all()
    
    # تأكد من أن slug فريد
    while queryset.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug


CONTENT_TYPES = {
    'articles': {
        'model': articles,
        'id_field': 'art_id',
        'subject_field': 'mysubject',
        'template': 'edit_article.html',
        'redirect_name': 'show_article',
        'types': ['الأمازيغية', 'تربية وتعليم', 'الثقافة العامة', 'علوم', 'القانون وحقوق الإنسان'],
        'form_class': ArticleForm,
    },
}

def advanced_transliterator(text):
    """
    تحويل النص إلى slug واضح ومقروء
    """
    if not text:
        return ""

    # تحويل النص إلى حروف صغيرة
    text = text.lower().strip()

    # استبدالات أقرب للنطق
    replacements = {
        'ء': '', 'آ': 'a', 'أ': 'a', 'إ': 'i', 'ئ': 'i', 'ؤ': 'o', 'ة': 'a',
        'ى': 'a', 'ٱ': 'a', 'ق': 'q', 'ك': 'k', 'ج': 'j', 'ش': 'sh', 'غ': 'gh',
        'ع': 'a', 'خ': 'kh', 'ح': 'h', 'ث': 'th', 'ص': 's', 'ض': 'd', 'ط': 't',
        'ظ': 'z', 'ذ': 'dh', 'ز': 'z', 'ر': 'r', 'د': 'd', 'س': 's', 'ب': 'b',
        'م': 'm', 'و': 'w', 'ت': 't', 'ن': 'n', 'ل': 'l', 'ف': 'f', 'ي': 'y',
        ' ': '_', '_': '_',

        # الفرنسية والرموز
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'à': 'a', 'â': 'a', 'ä': 'a',
        'î': 'i', 'ï': 'i', 'ô': 'o', 'ö': 'o', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'œ': 'oe', 'æ': 'ae',
        '/': '_', '\\': '_', ':': '_', ',': '_', '!': '', '?': '', '؟': '',
        '،': '_', '؛': '_', '"': '', "'": '', '«': '', '»': ''
    }

    for char, repl in replacements.items():
        text = text.replace(char, repl)

    # إزالة التشكيل
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])

    # السماح فقط بـ a-z و 0-9 و "_"
    text = re.sub(r'[^a-z0-9_]', '', text)

    # تقليل الشرطات/underscores
    text = re.sub(r'_+', '_', text).strip('_')

    return text

def edit_content(request, content_type, slug):
    
    config = CONTENT_TYPES.get(content_type)
    if not config:
        return HttpResponseNotFound("نوع المحتوى غير موجود")

    ModelClass = config['model']
    content = get_object_or_404(ModelClass, slug=slug)

    # حفظ القيم الأصلية للصور قبل أي تعديل
    original_myimage = content.myimage
    
    if hasattr(content, 'autre'):
        original_autre = content.autre

    # جلب التعليقات المرتبطة بالمقال
    content_comments = []
    comment_forms = []

    if content_type == 'articles':
        content_comments = comments.objects.filter(page_title=content.title)
        for comment in content_comments:
            comment_forms.append(CommentForm(instance=comment))

    if request.method == 'POST':
        # التحقق مما إذا كان الطلب لتعديل مقال أو تعليق
        if 'comment_id' in request.POST:
            # هذا طلب لتعديل تعليق
            comment_id = request.POST.get('comment_id')
            try:
                comment_obj = comments.objects.get(cmt_id=comment_id)
                comment_form = CommentForm(request.POST, instance=comment_obj)
                if comment_form.is_valid():
                    # تحديث حقل updated_at قبل الحفظ
                    comment_obj.updated_at = timezone.now()
                    comment_form.save()
                    messages.success(request, 'تم تحديث التعليق بنجاح')
                    return redirect(request.path)
                else:
                    messages.error(request, 'حدث خطأ في تحديث التعليق')
                    # إضافة أخطاء النموذج للرسائل
                    for field, errors in comment_form.errors.items():
                        for error in errors:
                            messages.error(request, f"{field}: {error}")
            except comments.DoesNotExist:
                messages.error(request, 'التعليق غير موجود')
        else:
            # هذا طلب لتعديل المقال
            form = config['form_class'](request.POST, request.FILES, instance=content)
            if form.is_valid():
                print("✅ النموذج صالح")
                print("📊 البيانات:", form.cleaned_data)
                
                try:
                    # حفظ المحتوى أولاً بدون commit
                    content = form.save(commit=False)
                    
                    # تأكد من أن slug ليس فارغاً
                    if not content.slug:
                        content.slug = slug
                    
                    # الحل الحاسم: التحقق من الملفات المرفوعة
                    print(f"📁 FILES: {request.FILES}")
                    print(f"📁 myimage في FILES: {'myimage' in request.FILES}")
                    
                    # إذا لم يتم رفع ملف جديد لـ myimage، استخدم القيمة الأصلية
                    if 'myimage' not in request.FILES or not request.FILES.get('myimage'):
                        content.myimage = original_myimage
                        print(f"🖼️ احتفظ بالصورة القديمة: {original_myimage}")
                    else:
                        print(f"🖼️ سيتم استخدام الصورة الجديدة: {request.FILES['myimage'].name}")
                    
                    # نفس المنطق لحقل autre إذا كان موجوداً
                    if hasattr(content, 'autre'):
                        if 'autre' not in request.FILES or not request.FILES.get('autre'):
                            content.autre = original_autre
                            print(f"🖼️ احتفظ بالصورة الإضافية القديمة: {original_autre}")
                    
                    # تحديث حقل updated_at
                    content.updated_at = timezone.now()
                    
                    # حفظ المحتوى
                    content.save()
                    print("💾 تم الحفظ بنجاح")
                    print(f"🖼️ الصورة بعد الحفظ: {content.myimage}")
                    
                    # حفظ الحقول many-to-many إذا وجدت
                    if hasattr(form, 'save_m2m'):
                        form.save_m2m()
                    
                    messages.success(request, 'تم تحديث المحتوى بنجاح')
                    return redirect(request.path)
                    
                except Exception as e:
                    logger.error(f"Error saving content: {e}")
                    messages.error(request, f'حدث خطأ في حفظ المحتوى: {str(e)}')
            else:
                print("❌ النموذج غير صالح:", form.errors)
                messages.error(request, 'حدث خطأ في تحديث المحتوى. يرجى التحقق من البيانات المدخلة.')

    else:
        form = config['form_class'](instance=content)

    # إذا لم تكن هناك نماذج تعليقات، أنشئها
    if not comment_forms and content_type == 'articles':
        for comment in content_comments:
            comment_forms.append(CommentForm(instance=comment))

    context = {
        'title': f'تعديل : {content.title}',
        
        # أرسل الكائن كاملاً والفورم
        'article': content,
        'form': form,  # هذا السطر المهم الناقص!
        'content_types': config['types'],
        'comments': zip(content_comments, comment_forms) if content_type == 'articles' else [],
        'comment_count': content_comments.count() if content_type == 'articles' else 0,
        'content_type': content_type,
        
        # معلومات التصحيح
        'debug_info': {
            'content_type': content_type,
            'myimage_value': content.myimage,
            'myimage_type': type(content.myimage),
            'myimage_exists': bool(content.myimage),
            'slug_value': content.slug
        }
    }

    return render(request, f'tifinar/auth/{content_type}/{config["template"]}', context)
        
def handle_uploaded_images(new_images, existing_images, slug, image_type):
    """معالجة الصور المحملة وحفظها"""
    image_names = []
    
    # استخدام advanced_transliterator لإنشاء أسماء الصور
    image_slug = advanced_transliterator(slug)  # هنا نستخدم الدالة
    
    # الاحتفاظ بالصور الموجودة إذا كانت موجودة
    if existing_images and isinstance(existing_images, str):
        image_names = [img.strip() for img in existing_images.split(',') if img.strip()]
    
    # إضافة الصور الجديدة
    for i, image in enumerate(new_images, start=1):
        ext = os.path.splitext(image.name)[1]
        # استخدام image_slug بدلاً من slug العادي
        new_name = f"{image_slug}_{image_type}_{i}{ext}"
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', new_name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        image_names.append(new_name)

    return ','.join(image_names) if image_names else ''
