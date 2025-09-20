import os
import re
import random
import unicodedata
import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone
from django.forms.utils import ErrorDict
from tifinar.myForms.cours.create_cours_form import CoursForm
from tifinar.models import cours

logger = logging.getLogger(__name__)

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

def simple_unique_id(length=4):
    """مولد ID قصير وبسيط (مثلاً 4 أرقام)"""
    return str(random.randint(10**(length-1), 10**length - 1))

def handle_uploaded_file(file, folder_name, title_slug, is_main_image=False):
    """معالجة ملف محمل وحفظه في المجلد الثابت"""
    if not file:
        return None
    
    # تنظيف اسم المجلد من الأحرف غير المسموحة
    if folder_name:
        # إزالة أي مسارات أو أحرف خطرة
        folder_name = re.sub(r'[^a-zA-Z0-9_-]', '', folder_name)
        if not folder_name:  # إذا أصبح فارغاً بعد التنظيف
            folder_name = "default_folder"
    else:
        folder_name = "default_folder"
    
    # إنشاء اسم فريد قصير
    unique_id = simple_unique_id(4)
    extension = file.name.split('.')[-1].lower() if '.' in file.name else 'file'
    
    # استخدام الـ slug المعدل أو اسم افتراضي
    clean_name = title_slug if title_slug and len(title_slug) > 2 else "cours"
    
    file_name = f"{clean_name}_{unique_id}.{extension}"
    
    # تحديد المسار المستهدف
    if is_main_image:
        target_dir = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'images', 'cours')
    else:
        target_dir = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'images', 'cours', folder_name)
    
    # التأكد من وجود المجلد
    os.makedirs(target_dir, exist_ok=True)
    
    # حفظ الملف
    file_path = os.path.join(target_dir, file_name)
    try:
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        logger.info(f"تم حفظ الملف: {file_path}")
        return file_name
    except Exception as e:
        logger.error(f"خطأ في حفظ الملف {file_path}: {str(e)}")
        return None
def create_cours(request):
    logger.info("بدء عملية إنشاء درس جديد")
    
    try:
        if request.method == 'POST':
            logger.info("طلب POST مستلم")
            form = CoursForm(request.POST, request.FILES)
            
            if form.is_valid():
                logger.info("النموذج صالح، بدء حفظ البيانات")
                obj = form.save(commit=False)
                
                # إنشاء slug من العنوان
                title = form.cleaned_data['title']
                logger.info(f"العنوان: {title}")
                
                if title:
                    obj.slug = advanced_transliterator(title)
                    logger.info(f"الـ slug المنشأ: {obj.slug}")
                    
                    # إذا كان قصير جداً
                    if len(obj.slug) < 3:
                        obj.slug = f"cours_{int(time.time())}"
                        logger.info(f"الـ slug البديل: {obj.slug}")
                
                # معالجة الصورة الرئيسية
                if 'myimage' in request.FILES:
                    logger.info("تم رفع صورة رئيسية")
                    image_file = request.FILES['myimage']
                    image_name = handle_uploaded_file(image_file, "", obj.slug, is_main_image=True)
                    if image_name:
                        obj.myimage = image_name
                        logger.info(f"تم حفظ الصورة الرئيسية: {image_name}")
                
                # معالجة الصور المتعددة
                images_files = request.FILES.getlist('images[]')
                image_names = request.POST.getlist('image_names[]')
                
                logger.info(f"عدد الصور المرفوعة: {len(images_files)}")
                logger.info(f"أسماء الصور: {image_names}")
                
                # الحصول على اسم المجلد وتنظيفه
                folder_name = form.cleaned_data.get('myfile', 'default_folder')
                if folder_name:
                    folder_name = re.sub(r'[^a-zA-Z0-9_-]', '', folder_name)
                    if not folder_name:
                        folder_name = 'default_folder'
                else:
                    folder_name = 'default_folder'
                
                logger.info(f"اسم المجلد بعد التنظيف: {folder_name}")
                
                saved_images = []
                
                for i, (image_file, image_name) in enumerate(zip(images_files, image_names)):
                    if image_file:
                        # استخدام الاسم المقدم أو إنشاء اسم افتراضي
                        custom_name = image_name.strip() if image_name else f"image_{i+1}"
                        # تنظيف الاسم من الأحرف غير المسموحة
                        custom_name = re.sub(r'[^a-zA-Z0-9_-]', '', custom_name)
                        if not custom_name:
                            custom_name = f"image_{i+1}"
                        
                        file_name = handle_uploaded_file(image_file, folder_name, custom_name, is_main_image=False)
                        if file_name:
                            saved_images.append(file_name)
                            logger.info(f"تم حفظ الصورة: {file_name}")
                        else:
                            logger.error(f"فشل في حفظ الصورة: {image_file.name}")
                
                # حفظ أسماء الصور في حقل images كسلسلة مفصولة بفواصل
                if saved_images:
                    obj.images = ", ".join(saved_images)
                    logger.info(f"أسماء الصور المحفوظة: {obj.images}")
                else:
                    logger.warning("لم يتم حفظ أي صور إضافية")
                
                # تعيين القيم الافتراضية
                obj.visibility_status = 'under_review'
                obj.created_at = timezone.now()
                obj.updated_at = timezone.now()
                
                logger.info("حفظ الكائن في قاعدة البيانات")
                obj.save()
                logger.info("تم حفظ الكائن بنجاح")
                
                return redirect('cours_edit')
            else:
                logger.error(f"أخطاء النموذج: {form.errors}")
                return render(request, 'tifinar/auth/cours/create_cours.html', {'form': form})
        else:
            form = CoursForm()
            logger.info("طلب GET، عرض النموذج الفارغ")
            return render(request, 'tifinar/auth/cours/create_cours.html', {'form': form})
            
    except Exception as e:
        logger.error(f"حدث خطأ: {str(e)}", exc_info=True)
        
        form = CoursForm(request.POST or None, request.FILES or None)
        
        error_msg = f"حدث خطأ غير متوقع في النظام: {str(e)}. يرجى المحاولة مرة أخرى."
        
        if not form._errors:
            form._errors = ErrorDict()
        
        if '__all__' not in form._errors:
            form._errors['__all__'] = form.error_class()
        
        form._errors['__all__'].append(error_msg)
        
        return render(request, 'tifinar/auth/cours/create_cours.html', {
            'form': form,
            'error_message': error_msg
        })

def test_form_validation():
    # اختتبار النموذج ببيانات اختبارية
    test_data = {
        'title': 'اختبار عنوان الدرس',
        'myfile': 'test_folder',
        'gender': 'all',
        'min_age': 5,
        'max_age': 15,
        'educational_level': '1',
        'dir': 'rtl',
        'the_type': 'with_board',
        'visibility_status': 'under_review',
    }
    
    form = CoursForm(data=test_data)
    print(f"النموذج صالح: {form.is_valid()}")
    if not form.is_valid():
        print(f"أخطاء النموذج: {form.errors}")
    
    return form.is_valid()

def check_saved_images():
    """للتحقق من وجود الصور المحفوظة"""
    base_dir = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'images', 'cours')
    
    print("المجلدات الموجودة:")
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path):
            print(f"المجلد: {item}")
            print(f"  الملفات: {os.listdir(item_path)}")