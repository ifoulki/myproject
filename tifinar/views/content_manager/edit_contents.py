from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from tifinar.models import articles, books, exams, videos, cours
from tifinar.forms import ArticleForm, BookForm, ExamForm, CoursForm, VideoForm
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
    'books': {
        'model': books,
        'id_field': 'book_id',
        'subject_field': 'mysubject',
        'template': 'edit_book.html',
        'redirect_name': 'show_book',
        'form_class': BookForm,
        'types': ['أدب', 'علوم', 'تاريخ', 'فلسفة']
    },
    'exams': {
        'model': exams,
        'id_field': 'exam_id',
        'subject_field': 'mysubject',
        'template': 'edit_exam.html',
        'redirect_name': 'show_exam',
        'form_class': ExamForm,
        'types': ['أدب', 'علوم', 'تاريخ', 'فلسفة']
    },
    'cours': {
        'model': cours,
        'id_field': 'cours_id',
        'subject_field': 'mysubject',
        'template': 'edit_cours.html',
        'redirect_name': 'show_cours',
        'form_class': CoursForm,
        'types': ['أدب', 'علوم', 'تاريخ', 'فلسفة']
    },
    'videos': {
        'model': videos,
        'id_field': 'vd_id',
        'template': 'edit_video.html',
        'form_class': VideoForm,
        'redirect_name': 'show_video',
        'types': ['أدب', 'علوم', 'تاريخ', 'فلسفة']
    },
}


def edit_content(request, content_type, slug):
    config = CONTENT_TYPES.get(content_type)
    if not config:
        return HttpResponseNotFound("نوع المحتوى غير موجود")

    ModelClass = config['model']
    content = get_object_or_404(ModelClass, slug=slug)

    if request.method == 'POST':
        form = config['form_class'](request.POST, request.FILES, instance=content)
        
        if form.is_valid():
            
            content = form.save(commit=False)
            image_fields = ['myimage', 'autre']            
            original_images = {field: getattr(content, field, '') for field in image_fields}
            
            for field in image_fields:
                if field in request.FILES and request.FILES[field]:
                    new_files = request.FILES.getlist(field)
                    processed_value = handle_uploaded_images(new_files, original_images[field], content.slug, field.split('_')[-1])
                    setattr(content, field, processed_value)
                else:
                    setattr(content, field, original_images[field])
            
            update_fields = [
                f.name for f in content._meta.get_fields()
                if f.concrete and 
                not f.primary_key and 
                not f.many_to_many and 
                not f.one_to_many and
                f.name not in image_fields
            ]
            
            content.save(update_fields=update_fields)
            
            for field in image_fields:
                if not (field in request.FILES and request.FILES[field]):
                    ModelClass.objects.filter(pk=content.pk).update(**{field: original_images[field]})
            
            if hasattr(form, 'save_m2m'):
                form.save_m2m()
            
            messages.success(request, 'تم تحديث المحتوى بنجاح')
            return redirect('tifinar:show_content', slug=content.slug)
    else:
        form = config['form_class'](instance=content)
    
    context = {
        'article': content,
        'form': form,
        'content_types': config['types']
    }
    
    return render(request, f'tifinar/auth/{content_type}/{config["template"]}', context)

def handle_uploaded_images(new_images, existing_images, slug, image_type):
    image_names = []
    if existing_images and isinstance(existing_images, str):
        image_names = existing_images.split(',')
    
    for i, image in enumerate(new_images, start=1):
        ext = os.path.splitext(image.name)[1]
        new_name = f"{slug}_{image_type}_{i}{ext}"
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', new_name)
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        image_names.append(new_name)
    
    return ','.join(image_names)
            
