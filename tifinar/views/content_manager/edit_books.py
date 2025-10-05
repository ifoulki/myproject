from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from tifinar.models import books, comments
from tifinar.forms import BookForm, CommentForm
from django.contrib import messages
import os
from django.conf import settings
import logging
import re
from django.db.models import Q
logger = logging.getLogger(__name__)
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib as mpl
from django.utils import timezone
import unicodedata

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

def normalize_text(text):
    """تطبيع النص لإزالة الاختلافات غير المرئية"""
    if not text:
        return ""
    # إزالة التشكيل والتحويل إلى شكل قياسي
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    # إزالة المسافات الزائدة والأحرف الخاصة
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return text

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


def handle_uploaded_images(new_images, existing_images, slug, image_type):
    """معالجة الصور المحملة وحفظها في مجلد static"""
    
    image_slug = advanced_transliterator(slug)
    
    # 🔥 استخدام أول مسار من STATICFILES_DIRS
    if settings.STATICFILES_DIRS:
        base_static_path = settings.STATICFILES_DIRS[0]
    else:
        base_static_path = os.path.join(settings.BASE_DIR, 'static')
    
    static_images_path = os.path.join(base_static_path, 'tifinar', 'images', 'books')
    
    print(f"📍 المسار المستهدف: {static_images_path}")
    print(f"📍 هل المجلد موجود؟ {os.path.exists(static_images_path)}")
    
    # 🔥 الخطوة 1: حذف جميع الصور القديمة
    if existing_images and isinstance(existing_images, str):
        old_images = [img.strip() for img in existing_images.split(',') if img.strip()]
        for old_image in old_images:
            old_path = os.path.join(static_images_path, old_image)
            print(f"🗑️ محاولة حذف: {old_path}")
            if os.path.exists(old_path):
                os.remove(old_path)
                print(f"🗑️ تم حذف الصورة القديمة: {old_image}")
            else:
                print(f"⚠️  الصورة القديمة غير موجودة: {old_image}")
    
    # 🔥 الخطوة 2: إضافة الصور الجديدة
    image_names = []
    
    for i, image in enumerate(new_images, start=1):
        ext = os.path.splitext(image.name)[1]
        new_name = f"{image_slug}_{image_type}_{i}{ext}"
        save_path = os.path.join(static_images_path, new_name)
        
        print(f"💾 محاولة حفظ الصورة في: {save_path}")
        
        # إنشاء المجلد إذا لم يكن موجوداً
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        print(f"📁 تم إنشاء/التأكد من المجلد: {os.path.dirname(save_path)}")
        
        # حفظ الصورة
        with open(save_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        image_names.append(new_name)
        
        # التحقق من الحفظ
        if os.path.exists(save_path):
            file_size = os.path.getsize(save_path)
            print(f"✅ تم حفظ الصورة بنجاح: {new_name} ({file_size} bytes)")
        else:
            print(f"❌ فشل في حفظ الصورة: {new_name}")

    return ','.join(image_names) if image_names else ''


CONTENT_TYPES = {
    'books': {
        'model': books,
        'id_field': 'books_id',
        'subject_field': 'mysubject',
        'template': 'edit_book.html',
        'redirect_name': 'show_book',
        'form_class': BookForm,
        'types': ['أدب', 'علوم', 'تاريخ', 'فلسفة']
    },
}
    
def edit_book(request, slug):
    # تحديد نوع المحتوى مباشرة داخل الدالة
    content_type = 'books'
    config = CONTENT_TYPES.get(content_type)
    
    if not config:
        return HttpResponseNotFound("نوع المحتوى غير موجود")

    ModelClass = config['model']
    content = get_object_or_404(ModelClass, slug=slug)

    # حفظ القيم الأصلية للصور قبل أي تعديل
    original_myimage = content.myimage
    if hasattr(content, 'autre'):
        original_autre = content.autre

    # جلب التعليقات المرتبطة بالكتاب
    content_comments = []
    comment_forms = []

    if content_type == 'books':
        print(f"=== بدء التحقق من التعليقات ===")
        print(f"عنوان الكتاب: '{content.title}'")
        print(f"slug الكتاب: '{slug}'")
        
        # تطبيع العناوين للمقارنة
        normalized_book_title = normalize_text(content.title)
        print(f"العنوان بعد التطبيع: '{normalized_book_title}'")
        
        # جلب جميع التعليقات غير NULL
        all_comments = comments.objects.filter(page_title__isnull=False)
        print(f"عدد التعليقات (غير NULL): {all_comments.count()}")
        
        # البحث بالتطابق الكامل فقط
        for comment in all_comments:
            normalized_comment_title = normalize_text(comment.page_title)
            
            # التطابق الكامل فقط - تم إزالة التطابق الجزئي
            exact_match = normalized_comment_title == normalized_book_title
            
            print(f"التعليق {comment.cmt_id}: '{comment.page_title}'")
            print(f"  تطبيع: '{normalized_comment_title}'")
            print(f"  تطابق تام؟ {exact_match}")
            
            if exact_match:
                content_comments.append(comment)
                print(f"  -> تمت الإضافة (تطابق كامل)")
            else:
                print(f"  -> لم تتم الإضافة (لا يوجد تطابق كامل)")
            print(f"  ---")
        
        print(f"عدد التعليقات المرتبطة: {len(content_comments)}")
        
        # إنشاء نماذج لكل تعليق
        for comment in content_comments:
            comment_forms.append(CommentForm(instance=comment))
            print(f"تم إنشاء نموذج للتعليق {comment.cmt_id}")

    if request.method == 'POST':
        # 🔥 طباعة جميع بيانات POST للتحقق
        print("=== بيانات POST المستلمة ===")
        for key, value in request.POST.items():
            print(f"{key}: {value}")
        print("=== نهاية بيانات POST ===")

        # التحقق مما إذا كان الطلب لتعديل كتاب أو تعليق
        if 'comment_id' in request.POST:
            # هذا طلب لتعديل تعليق
            comment_id = request.POST.get('comment_id')
            try:
                comment_obj = comments.objects.get(cmt_id=comment_id)
                
                # تحديث الحقول يدوياً لتجنب مشاكل النموذج
                comment_obj.author_name = request.POST.get('author_name')
                comment_obj.author_email = request.POST.get('author_email')
                comment_obj.cmt_subject = request.POST.get('cmt_subject')
                comment_obj.visibility_status = request.POST.get('visibility_status')
                comment_obj.updated_at = timezone.now()
                
                comment_obj.save()
                messages.success(request, 'تم تحديث التعليق بنجاح')
                print(f"تم تحديث التعليق {comment_id} بنجاح")
                return redirect(request.path)

            except comments.DoesNotExist:
                error_msg = 'التعليق غير موجود'
                messages.error(request, error_msg)
                print(error_msg)
            except Exception as e:
                error_msg = f'حدث خطأ في تحديث التعليق: {str(e)}'
                messages.error(request, error_msg)
                print(error_msg)
                
        else:
            # هذا طلب لتعديل الكتاب
            form = config['form_class'](request.POST, request.FILES, instance=content)
            print(f"📝 النموذج صالح؟ {form.is_valid()}")
            if form.errors:
                print(f"📝 أخطاء النموذج: {form.errors}")
            
            if form.is_valid():
                try:
                    content = form.save(commit=False)
                    
                    # 🔥 الحل الجذري: تحديث visibility_status مباشرة من request.POST
                    visibility_status = request.POST.get('visibility_status')
                    print(f"🔍 visibility_status من POST: {visibility_status}")
                    
                    if visibility_status:
                        content.visibility_status = visibility_status
                        print(f"✅ تم تعيين visibility_status إلى: {visibility_status}")
                    else:
                        # إذا لم يتم إرسال القيمة، استخدم القيمة الحالية
                        print(f"⚠️  لم يتم إرسال visibility_status، الاستمرار بالقيمة الحالية: {content.visibility_status}")
                    
                    # تحديث حقل updated_at
                    content.updated_at = timezone.now()
                    
                    # الحل: التحقق من الملفات المرفوعة والحفاظ على القيم الأصلية
                    print(f"📁 FILES: {request.FILES}")
                    print(f"📁 myimage في FILES: {'myimage' in request.FILES}")
                    
                    # إذا لم يتم رفع ملف جديد لـ myimage، استخدم القيمة الأصلية
                    if 'myimage' not in request.FILES or not request.FILES.get('myimage'):
                        content.myimage = original_myimage
                        print(f"🖼️ احتفظ بالصورة القديمة: {original_myimage}")
                    else:
                        print(f"🖼️ سيتم استخدام الصورة الجديدة: {request.FILES['myimage'].name}")
                        # استخدام advanced_transliterator لأسماء الصور الجديدة
                        if request.FILES.get('myimage'):
                            new_files = request.FILES.getlist('myimage')
                            processed_value = handle_uploaded_images(
                                new_files, original_myimage, content.slug, 'myimage'
                            )
                            content.myimage = processed_value
                    
                    # نفس المنطق لحقل autre إذا كان موجوداً
                    if hasattr(content, 'autre'):
                        if 'autre' not in request.FILES or not request.FILES.get('autre'):
                            content.autre = original_autre
                            print(f"🖼️ احتفظ بالصورة الإضافية القديمة: {original_autre}")
                        else:
                            # استخدام advanced_transliterator لأسماء الصور الجديدة
                            if request.FILES.get('autre'):
                                new_files = request.FILES.getlist('autre')
                                processed_value = handle_uploaded_images(
                                    new_files, original_autre, content.slug, 'autre'
                                )
                                content.autre = processed_value
                    
                    # 🔥 تأكد من حفظ visibility_status
                    print(f"🔍 visibility_status قبل الحفظ: {content.visibility_status}")
                    
                    content.save()

                    if hasattr(form, 'save_m2m'):
                        form.save_m2m()

                    # 🔥 تحقق من القيمة في قاعدة البيانات
                    try:
                        from django.db import connection
                        with connection.cursor() as cursor:
                            cursor.execute("SELECT visibility_status FROM books WHERE VD_id = %s", [content.books_id])
                            db_status = cursor.fetchone()
                            print(f"🗄️  القيمة في قاعدة البيانات: {db_status}")
                    except Exception as db_error:
                        print(f"❌ خطأ في التحقق من قاعدة البيانات: {db_error}")

                    messages.success(request, 'تم تحديث الكتاب بنجاح')
                    print(f"✅ تم تحديث الكتاب {content.title} بنجاح")
                    print(f"🖼️ الصورة بعد الحفظ: {content.myimage}")
                    print(f"🔍 visibility_status بعد الحفظ: {content.visibility_status}")
                    return redirect(request.path)
                    
                except Exception as e:
                    error_msg = f'حدث خطأ في تحديث الكتاب: {str(e)}'
                    messages.error(request, error_msg)
                    print(error_msg)
            else:
                error_msg = 'بيانات النموذج غير صالحة'
                messages.error(request, error_msg)
                print(error_msg)
                for field, errors in form.errors.items():
                    for error in errors:
                        error_detail = f"{field}: {error}"
                        messages.error(request, error_detail)
                        print(error_detail)

    else:
        form = config['form_class'](instance=content)

    # إذا لم تكن هناك نماذج تعليقات، أنشئها
    if not comment_forms and content_type == 'books':
        for comment in content_comments:
            comment_forms.append(CommentForm(instance=comment))

    context = {
        'book': content,
        'title': content.title,
        'description': content.mydescription,
        'form': form,
        'content_types': config['types'],
        'comments': zip(content_comments, comment_forms) if content_type == 'books' else [],
        'comment_count': len(content_comments) if content_type == 'books' else 0,
        'current_visibility': content.visibility_status  # 🔥 إرسال القيمة الحالية للقالب
    }

    print(f"تم تحضير context مع {len(content_comments)} تعليقات")
    
    return render(request, f'tifinar/auth/books/edit_book.html', context)