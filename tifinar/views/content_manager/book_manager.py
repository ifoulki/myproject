from django.shortcuts import render, redirect
from tifinar.myForms.book.create_book_form import BookForm
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import re
import os
from django.contrib import messages
from django.http import HttpResponseForbidden
import unicodedata
import shutil
from django.core.exceptions import ValidationError

def handle_uploaded_file(request, field_name, title_slug):
    """معالجة ملف محمل وحفظه في المجلد الثابت"""
    if field_name in request.FILES:
        file = request.FILES[field_name]
        
        # تحقق إذا كان file كائن ملف حقيقي
        if hasattr(file, 'name') and hasattr(file, 'size'):
            sanitized_title_slug = sanitize_file_name(title_slug)
            extension = file.name.split('.')[-1].lower() if '.' in file.name else ''
            file_name = generate_file_name(sanitized_title_slug, 0, extension, field_name)
            
            # المسار الجديد في المجلد الثابت
            if field_name == 'myimage':
                target_dir = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'images', 'books')
            else:
                target_dir = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'attachments', 'books')
            
            # تأكد من وجود المجلد
            os.makedirs(target_dir, exist_ok=True)
            
            # المسار الكامل للملف
            file_path = os.path.join(target_dir, file_name)
            
            print(f"سيتم حفظ الملف في: {file_path}")
            
            # حفظ الملف
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # تخزين المسار النسبي للعرض في القالب
            if field_name == 'myimage':
                return f'tifinar/images/books/{file_name}'
            else:
                return f'tifinar/attachments/books/{file_name}'
    
    return None

def sanitize_file_name(file_name):
    """تنظيف اسم الملف من الأحرف غير المرغوبة"""
    normalized = unicodedata.normalize('NFKD', file_name)
    ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')
    clean_name = re.sub(r'[^A-Za-z0-9_\-]', '', ascii_text)
    return clean_name.lower()

def generate_file_name(title_slug, index, extension, prefix):
    """إنشاء اسم ملف وفق القواعد المطلوبة"""
    if prefix == 'autre':
        return f"image_de_{title_slug}_{index + 1}.{extension}"
    else:
        return f"{title_slug}_{index + 1}.{extension}"

def create_book(request):
    try:
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    obj = form.save()
                    return redirect('edit_article', slug=obj.slug)
                except ValidationError as e:
                    # إضافة الخطأ إلى النموذج لعرضه للمستخدم
                    form.add_error(None, e)
            
            return render(request, 'tifinar/auth/books/create_book.html', {'form': form})
        
        else:
            form = BookForm()
            return render(request, 'tifinar/auth/books/create_book.html', {'form': form})
            
    except Exception as e:
        # في حالة أي خطأ غير متوقع، نعود برسالة واضحة
        form = BookForm()
        form.add_error(None, "حدث خطأ غير متوقع في النظام. يرجى المحاولة مرة أخرى.")
        return render(request, 'tifinar/auth/books/create_book.html', {
            'form': form,
            'error_message': "عذراً، حدث خطأ في النظام. تم إبلاغ الفنيين بهذه المشكلة."
        })