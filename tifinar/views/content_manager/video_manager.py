from django.shortcuts import render, redirect,get_object_or_404
from tifinar.myForms.video.create_video_form import VideoForm
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings  # أضف هذا
from django.utils.text import slugify  # أضف هذا
import re
import os
from django.contrib import messages
from django.http import HttpResponseForbidden
import unicodedata
import shutil

def handle_uploaded_files(request, field_name, title_slug):
    """معالجة الملفات المحملة وحفظها في المجلد الثابت"""
    paths = []
    
    if field_name in request.FILES:
        files = request.FILES.getlist(field_name)
        
        for index, file in enumerate(files):
            sanitized_title_slug = sanitize_file_name(title_slug)
            extension = file.name.split('.')[-1].lower()
            file_name = generate_file_name(sanitized_title_slug, index, extension, field_name)
            
            # المسار الجديد في المجلد الثابت
            if field_name == 'myimage':
                target_dir = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'images', 'videos')

            else:
                target_dir = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'attachments', 'videos')
            
            # تأكد من وجود المجلد
            os.makedirs(target_dir, exist_ok=True)
            
            # المسار الكامل للملف
            file_path = os.path.join(target_dir, file_name)
            
            print(f"سيتم حفظ الملف في: {file_path}")  # للتصحيح
            
            # حفظ الملف
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # تخزين المسار النسبي للعرض في القالب
            if field_name == 'myimage':
                relative_path = f'tifinar/images/videos/{file_name}'
            else:
                relative_path = f'tifinar/attachments/videos/{file_name}'
            
            paths.append(relative_path)

    
    return ','.join(paths) if paths else None

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

from django.shortcuts import render, redirect,get_object_or_404
from tifinar.myForms.video.create_video_form import VideoForm
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.text import slugify
import re
import os
from django.contrib import messages
from django.http import HttpResponseForbidden
import unicodedata
import shutil

def convert_to_embed_url(url):
    """تحويل رابط YouTube إلى تنسيق embed"""
    if not url:
        return url
    
    # تحويل روابط youtu.be
    if 'youtu.be' in url:
        video_id = url.split('/')[-1].split('?')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    
    # تحويل روابط youtube.com
    if 'youtube.com' in url:
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}'
    
    # إذا كان الرابط بالفعل بتنسيق embed أو غير معروف
    return url

def create_video(request):
    """
    دالة مخصصة لإنشاء الفيديوهات فقط
    """
    # إنشاء المجلدات داخل الدالة
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'videos/images'), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'videos/attachments'), exist_ok=True)
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            
            # تحويل رابط YouTube إلى تنسيق embed إذا كان موجوداً
            if 'mysubject' in form.cleaned_data and form.cleaned_data['mysubject']:
                obj.mysubject = convert_to_embed_url(form.cleaned_data['mysubject'])
            
            # إنشاء slug من العنوان (مرة واحدة فقط)
            title = form.cleaned_data['title']
            if title:
                clean = re.sub(r'[^\w\s-]', '', title)
                clean = clean.replace(' ', '_')
                obj.slug = slugify(clean, allow_unicode=True)
            
            # معالجة الملفات
            if 'myimage' in request.FILES:
                image_path = handle_uploaded_files(request, 'myimage', obj.slug)
                obj.myimage = image_path
            
            if 'autre' in request.FILES:
                attachment_path = handle_uploaded_files(request, 'autre', obj.slug)
                obj.autre = attachment_path
            
            # تعيين القيم الافتراضية
            obj.visibility_status = 'under_review'
            obj.created_at = timezone.now()
            obj.updated_at = timezone.now()
            
            obj.save()
            return redirect('edit_video', slug=obj.slug) 

        else:
            # أضف هذا لرؤية الأخطاء في الكونسول
            print("Form errors:", form.errors)
            print("Form non-field errors:", form.non_field_errors())
            # أضف هذا لعرض الأخطاء في القالب أيضاً
            return render(request, 'tifinar/auth/videos/create_video.html', {
                'form': form,
                'errors': form.errors
            })
    else:
        form = VideoForm()
    
    return render(request, 'tifinar/auth/videos/create_video.html', {'form': form})

