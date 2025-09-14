from django.shortcuts import render, redirect
from tifinar.myForms.book.create_book_form import BookForm
from django.utils import timezone
from django.conf import settings
import re
import os
from django.contrib import messages
from django.http import HttpResponseForbidden
import unicodedata
import shutil
from django.core.exceptions import ValidationError
import random
import time

def simple_unique_id(length=4):
    """مولد ID قصير وبسيط (مثلاً 4 أرقام)"""
    return str(random.randint(10**(length-1), 10**length - 1))

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

def handle_uploaded_file(request, field_name, title_slug):
    """معالجة ملف محمل وحفظه في المجلد الثابت"""
    print(f"📁 بدء معالجة الملف: {field_name}, slug: {title_slug}")
    
    if field_name in request.FILES:
        file = request.FILES[field_name]
        print(f"📄 الملف الأصلي: {file.name}")
        
        # إنشاء اسم فريد قصير
        unique_id = simple_unique_id(4)
        extension = file.name.split('.')[-1].lower() if '.' in file.name else 'file'
        
        # استخدام الـ slug المعدل أو اسم افتراضي
        clean_name = title_slug if title_slug and len(title_slug) > 2 else "book"
        
        file_name = f"{clean_name}_{unique_id}.{extension}"
        print(f"📝 الاسم الجديد: {file_name}")
        
        # المسار المستهدف (لكن نخزن غير اسم الملف في قاعدة البيانات)
        if field_name == 'myimage':
            target_dir = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'images', 'books')
        else:
            target_dir = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'ebookZone')
        
        os.makedirs(target_dir, exist_ok=True)
        
        # حفظ الملف
        file_path = os.path.join(target_dir, file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        print(f"✅ تم حفظ الملف فعلياً: {file_path}")
        return file_name  # ✅ نرجع غير الاسم + الامتداد
    
    return None

def create_book(request):
    try:
        # إنشاء المجلدات
        os.makedirs(os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'images', 'books'), exist_ok=True)
        os.makedirs(os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'ebookZone'), exist_ok=True)
        
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    obj = form.save(commit=False)  # لا تحفظ مباشرة
                    
                    # إنشاء slug من العنوان
                    if not obj.slug:
                        title = form.cleaned_data['title']
                        if title:
                            obj.slug = advanced_transliterator(title)
                            print(f"📝 العنوان الأصلي: {title}")
                            print(f"✅ الـ slug النهائي: {obj.slug}")
                            
                            # إذا كان قصير جداً
                            if len(obj.slug) < 3:
                                obj.slug = f"book_{int(time.time())}"
                                print(f"⚠️ تم استخدام slug بديل: {obj.slug}")
                    
                    # معالجة الملفات
                    if 'myimage' in request.FILES:
                        if 'myimage' in form.cleaned_data:
                            del form.cleaned_data['myimage']
                        
                        image_file_name = handle_uploaded_file(request, 'myimage', obj.slug)
                        if image_file_name:
                            obj.myimage = image_file_name  # ✅ فقط الاسم
                            print(f"✅ تم تعيين myimage: {obj.myimage}")
                        else:
                            print("❌ فشل معالجة الصورة")
                    else:
                        print("⚠️ لم يتم رفع أي صورة")
                    
                    if 'autre' in request.FILES:
                        if 'autre' in form.cleaned_data:
                            del form.cleaned_data['autre']
                        
                        attachment_file_name = handle_uploaded_file(request, 'autre', obj.slug)
                        if attachment_file_name:
                            obj.autre = attachment_file_name  # ✅ فقط الاسم
                            print(f"✅ تم تعيين autre: {obj.autre}")
                        else:
                            print("❌ فشل معالجة المرفق")
                    
                    # تعيين القيم الافتراضية
                    obj.created_at = timezone.now()
                    obj.updated_at = timezone.now()
                    
                    obj.save()  # حفظ الكائن
                    print("✅ تم حفظ الكائن بنجاح")
                    
                    return redirect('edit_book', slug=obj.slug)
                except ValidationError as e:
                    form.add_error(None, e)
                    print(f"❌ خطأ في التحقق: {e}")
                except Exception as e:
                    form.add_error(None, f"حدث خطأ أثناء معالجة البيانات: {str(e)}")
                    print(f"❌ خطأ غير متوقع: {str(e)}")
            
            return render(request, 'tifinar/auth/books/create_book.html', {'form': form})
        
        else:
            form = BookForm()
            return render(request, 'tifinar/auth/books/create_book.html', {'form': form})
            
    except Exception as e:
        form = BookForm()
        form.add_error(None, f"حدث خطأ غير متوقع في النظام: {str(e)}. يرجى المحاولة مرة أخرى.")
        print(f"❌ خطأ في الدالة الرئيسية: {str(e)}")
        return render(request, 'tifinar/auth/books/create_book.html', {
            'form': form,
            'error_message': "عذراً، حدث خطأ في النظام. تم إبلاغ الفنيين بهذه المشكلة."
        })
