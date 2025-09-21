from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings
from tifinar.myForms.exam.create_exam_form import ExamForm
from tifinar.models import exams
import os
import re
import unicodedata
import uuid
import logging

logger = logging.getLogger(__name__)

def advanced_transliterator(text):
    """
    تحويل النص العربي إلى slug إنجليزي واضح ومقروء
    """
    if not text:
        return ""

    # تحويل النص إلى حروف صغيرة
    text = text.lower().strip()

    # استبدالات أقرب للنطق العربي
    arabic_replacements = {
        'ء': '', 'آ': 'a', 'أ': 'a', 'إ': 'i', 'ئ': 'e', 'ؤ': 'o', 'ة': 'a',
        'ى': 'a', 'ٱ': 'a', 'ق': 'k', 'ك': 'k', 'ج': 'j', 'ش': 'sh', 'غ': 'gh',
        'ع': 'a', 'خ': 'kh', 'ح': 'h', 'ث': 'th', 'ص': 's', 'ض': 'd', 'ط': 't',
        'ظ': 'z', 'ذ': 'th', 'ز': 'z', 'ر': 'r', 'د': 'd', 'س': 's', 'ب': 'b',
        'م': 'm', 'و': 'w', 'ت': 't', 'ن': 'n', 'ل': 'l', 'ف': 'f', 'ي': 'y',
        'ه': 'h', 'ا': 'a', ' ': '_', '_': '_', '-': '_',
        
        # الفرنسية
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'à': 'a', 'â': 'a', 'ä': 'a',
        'î': 'i', 'ï': 'i', 'ô': 'o', 'ö': 'o', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'œ': 'oe', 'æ': 'ae',
    }

    for char, repl in arabic_replacements.items():
        text = text.replace(char, repl)

    # إزالة التشكيل والحركات
    text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])

    # استبدال الرموز الخاصة
    symbol_replacements = {
        '/': '_', '\\': '_', ':': '_', ',': '_', '!': '', '?': '', '؟': '',
        '،': '_', '؛': '_', '"': '', "'": '', '«': '', '»': '', '[': '', ']': '',
        '{': '', '}': '', '(': '', ')': '', '*': '', '#': '', '@': '', '$': '',
        '%': '', '^': '', '&': '', '=': '', '+': '', '<': '', '>': '', '~': '',
        '`': ''
    }

    for char, repl in symbol_replacements.items():
        text = text.replace(char, repl)

    # السماح فقط بـ a-z, 0-9, وشرطات وشرطات سفلية ← انقل هذا إلى النهاية!
    text = re.sub(r'[^a-z0-9_-]', '', text)

    # تقليل الشرطات/الشرطات السفلية المتتالية
    text = re.sub(r'[-_]+', '_', text).strip('-_')

    return text

def generate_unique_slug(title, model, instance=None):
    """
    إنشاء slug فريد بناءً على العنوان
    """
    base_slug = advanced_transliterator(title)
    
    # إذا كان العنوان فارغاً أو النتيجة قصيرة جداً
    if not base_slug or len(base_slug) < 3:
        base_slug = f"exam-{int(timezone.now().timestamp())}"
    
    slug = base_slug
    counter = 1
    
    # التحقق من التكرار
    while True:
        if instance:
            exists = model.objects.filter(slug=slug).exclude(pk=instance.pk).exists()
        else:
            exists = model.objects.filter(slug=slug).exists()
        
        if not exists:
            break
        
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug

def generate_image_filename(title, original_filename):
    """
    إنشاء اسم ملف صورة واضح بناءً على العنوان
    """
    # استخراج الامتداد من الملف الأصلي
    file_extension = os.path.splitext(original_filename)[1].lower()
    
    # إنشاء base name من العنوان
    base_name = advanced_transliterator(title)
    
    # إذا كان العنوان فارغاً أو النتيجة قصيرة جداً
    if not base_name or len(base_name) < 3:
        base_name = f"exam_{int(timezone.now().timestamp())}"
    
    # استبدال الشرطات بشرطات سفلية
    base_name = base_name.replace('-', '_')
    
    # إضافة معرف فريد قصير
    unique_id = uuid.uuid4().hex[:3]
    
    return f"{base_name}_{unique_id}{file_extension}"


def generate_image_filename(title, original_filename):
    """
    إنشاء اسم ملف صورة واضح بناءً على العنوان
    """
    # استخراج الامتداد من الملف الأصلي
    file_extension = os.path.splitext(original_filename)[1].lower()
    
    # إنشاء base name من العنوان مع استخدام الشرطات السفلية
    base_name = advanced_transliterator(title).replace('-', '_')
    
    # إذا كان العنوان فارغاً أو قصيراً
    if not base_name or len(base_name) < 3:
        base_name = f"exam_{int(timezone.now().timestamp())}"
    
    # إضافة معرف فريد قصير
    unique_id = uuid.uuid4().hex[:3]
    
    return f"{base_name}_{unique_id}{file_extension}"

def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST, request.FILES)
        print(f"📋 النموذج received: {request.POST}")
        print(f"📁 الملفات received: {request.FILES}")
        
        if form.is_valid():
            print("✅ النموذج صالح!")
            try:
                exam = form.save(commit=False)
                
                # إنشاء slug جميل وفريد
                title = form.cleaned_data.get('title', '')
                exam.slug = generate_unique_slug(title, exams)
                print(f"✅ تم إنشاء slug: {exam.slug}")
                
                # معالجة تحميل الصورة
                if 'myimage' in request.FILES:
                    image_file = request.FILES['myimage']
                    original_filename = image_file.name
                    print(f"📁 الملف الأصلي: {original_filename}")
                    print(f"📝 العنوان: {title}")
                    
                    # إنشاء اسم جديد للصورة
                    file_extension = os.path.splitext(original_filename)[1].lower()
                    base_name = advanced_transliterator(title)
                    
                    if not base_name or len(base_name) < 3:
                        base_name = f"exam_{int(timezone.now().timestamp())}"
                    
                    base_name = base_name.replace('-', '_')
                    new_filename = f"{base_name}_{uuid.uuid4().hex[:3]}{file_extension}"
                    print(f"🆕 الاسم الجديد: {new_filename}")
                    
                    # المسار الكامل للحفظ
                    target_path = os.path.join('tifinar', 'static', 'tifinar', 'images', 'exams', new_filename)
                    full_path = os.path.join(settings.BASE_DIR, target_path)
                    print(f"📂 المسار الكامل: {full_path}")
                    
                    # إنشاء المجلد إذا لم يكن موجوداً
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    
                    # حفظ الصورة
                    with open(full_path, 'wb+') as destination:
                        for chunk in image_file.chunks():
                            destination.write(chunk)
                    
                    print(f"✅ تم حفظ الصورة في: {full_path}")
                    
                    # حفظ المسار في قاعدة البيانات
                    exam.myimage = target_path
                    print(f"💾 تم حفظ في DB: {exam.myimage}")
                else:
                    print("⚠️ لم يتم رفع أي صورة")
                
                # الحقول الأخرى - التحقق من القيم
                exam.visibility_status = 'under_review'
                print(f"🔍 قيمة visibility_status: '{exam.visibility_status}'")
                print(f"🔍 نوع visibility_status: {type(exam.visibility_status)}")
                
                exam.created_at = timezone.now()
                exam.updated_at = timezone.now()
                
                if not exam.min_age:
                    exam.min_age = 2
                if not exam.max_age:
                    exam.max_age = 75
                if not exam.gender:
                    exam.gender = 'all'
                if not exam.educational_level:
                    exam.educational_level = '0'
                
                # التحقق النهائي من جميع القيم قبل الحفظ
                print(f"🎯 القيم النهائية قبل الحفظ:")
                print(f"   - visibility_status: '{exam.visibility_status}'")
                print(f"   - gender: '{exam.gender}'")
                print(f"   - educational_level: '{exam.educational_level}'")
                print(f"   - min_age: {exam.min_age}")
                print(f"   - max_age: {exam.max_age}")
                
                # الحفظ النهائي
                exam.save()
                print(f"🎉 تم حفظ الاختبار كاملاً: {exam.exam_id}")
                
                messages.success(request, '✅ تم إنشاء الاختبار بنجاح!')
                return redirect('edit_exam', slug=exam.slug)
                
            except Exception as e:
                print(f"❌ خطأ في الحفظ: {str(e)}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'❌ حدث خطأ أثناء حفظ البيانات: {str(e)}')
        else:
            print(f"❌ النموذج غير صالح! الأخطاء:")
            for field, errors in form.errors.items():
                print(f"   {field}: {errors}")
            print(f"📊 بيانات النموذج: {form.data}")
            messages.error(request, '❌ يرجى تصحيح الأخطاء في النموذج.')
            
            # إرجاع النموذج مع الأخطاء لعرضها في القالب
            return render(request, 'tifinar/auth/exams/create_exam.html', {
                'form': form,
                'errors': form.errors
            })
    else:
        form = ExamForm()
        form.fields['min_age'].initial = 2
        form.fields['max_age'].initial = 75
        form.fields['gender'].initial = 'all'
        form.fields['educational_level'].initial = '0'
        print("📝 طلب GET - عرض النموذج الفارغ")
    
    return render(request, 'tifinar/auth/exams/create_exam.html', {'form': form})

def delete_exam_image(request, exam_id):
    """حذف صورة الاختبار"""
    exam = get_object_or_404(exams, exam_id=exam_id)
    
    if request.method == 'POST':
        try:
            if exam.myimage:
                fs = FileSystemStorage()
                if fs.exists(exam.myimage):
                    fs.delete(exam.myimage)
                    logger.info(f"تم حذف الصورة: {exam.myimage}")
                
                exam.myimage = None
                exam.save()
                
                messages.success(request, '✅ تم حذف الصورة بنجاح!')
            else:
                messages.warning(request, '⚠️ لا توجد صورة لحذفها!')
                
        except Exception as e:
            logger.error(f"خطأ في حذف الصورة: {str(e)}")
            messages.error(request, '❌ حدث خطأ أثناء حذف الصورة!')
    
    return redirect('edit_exam', exam_id=exam_id)

def preview_slug(request):
    """معاينة slug قبل الحفظ"""
    if request.method == 'GET' and 'title' in request.GET:
        title = request.GET['title']
        slug = generate_unique_slug(title, exams)
        return JsonResponse({'slug': slug})
    return JsonResponse({'error': 'طلب غير صالح'})

def check_exam_slug(request):
    """التحقق من توفر slug"""
    if request.method == 'GET' and 'slug' in request.GET:
        slug = request.GET['slug']
        exists = exams.objects.filter(slug=slug).exists()
        return JsonResponse({'exists': exists, 'available': not exists})
    return JsonResponse({'error': 'طلب غير صالح'})



def edit_exam(request, slug):
    """تعديل اختبار موجود"""
    exam = get_object_or_404(exams, slug=slug)
    
    if request.method == 'POST':
        form = ExamForm(request.POST, request.FILES, instance=exam)
        if form.is_valid():
            try:
                updated_exam = form.save(commit=False)
                
                # معالجة الصورة إذا تم رفع جديدة
                if 'myimage' in request.FILES:
                    image_file = request.FILES['myimage']
                    original_filename = image_file.name
                    
                    # إنشاء اسم جديد للصورة
                    file_extension = os.path.splitext(original_filename)[1].lower()
                    base_name = advanced_transliterator(updated_exam.title)
                    
                    if not base_name or len(base_name) < 3:
                        base_name = f"exam_{int(timezone.now().timestamp())}"
                    
                    base_name = base_name.replace('-', '_')
                    new_filename = f"{base_name}_{uuid.uuid4().hex[:4]}{file_extension}"
                    
                    # المسار الكامل للحفظ
                    target_path = os.path.join('tifinar', 'static', 'tifinar', 'images', 'exams', new_filename)
                    full_path = os.path.join(settings.BASE_DIR, target_path)
                    
                    # إنشاء المجلد إذا لم يكن موجوداً
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                    
                    # حفظ الصورة
                    with open(full_path, 'wb+') as destination:
                        for chunk in image_file.chunks():
                            destination.write(chunk)
                    
                    # حفظ المسار في قاعدة البيانات
                    updated_exam.myimage = target_path
                
                updated_exam.updated_at = timezone.now()
                updated_exam.save()
                
                messages.success(request, '✅ تم تحديث الاختبار بنجاح!')
                return redirect('edit_exam', slug=updated_exam.slug)
                
            except Exception as e:
                messages.error(request, f'❌ حدث خطأ أثناء التحديث: {str(e)}')
        else:
            messages.error(request, '❌ يرجى تصحيح الأخطاء في النموذج.')
    else:
        form = ExamForm(instance=exam)
    
    return render(request, 'tifinar/auth/exams/edit_exam.html', {
        'form': form,
        'exam': exam
    })