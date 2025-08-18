from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from .models import articles, books, exams, videos, cours, comments, ArticleReaction
from .forms import CommentForm, ArticleForm, BookForm, ExamForm, CoursForm, VideoForm,UserEditForm
from django.contrib import messages
from django.http import FileResponse, Http404
import os
from django.conf import settings
from urllib.parse import unquote
from django.utils import timezone
import logging
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger(__name__)

from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.text import slugify
import re

import matplotlib.pyplot as plt
from io import BytesIO
import base64
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib as mpl
from django.contrib.auth.decorators import login_required

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if 'clear_image' in request.POST:
                request.user.profile_image.delete()
            form.save()
            messages.success(request, 'تم تحديث البيانات بنجاح')
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    
    return render(request, 'tifinar/auth/edit_user.html', {'form': form})

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

def create_content(request, content_type):
    if content_type == 'articles':
        FormClass = ArticleForm
        template = 'tifinar/auth/articles/create_article.html'
        redirect_view = 'tifinar:edit_article'
    elif content_type == 'books':
        FormClass = BookForm
        template = 'tifinar/auth/books/create_book.html'
        redirect_view = 'tifinar:edit_book'
    elif content_type == 'cours':
        FormClass = CoursForm
        template = 'tifinar/auth/cours/create_cours.html'
        redirect_view = 'tifinar:edit_cours'
    elif content_type == 'videos':
        FormClass = VideoForm
        template = 'tifinar/auth/videos/create_video.html'
        redirect_view = 'tifinar:edit_video'
    elif content_type == 'exams':
        FormClass = ExamForm
        template = 'tifinar/auth/exams/create_exam.html'
        redirect_view = 'tifinar:edit_exam'
    else:
        return render(request, '404.html', status=404)

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)

            title = form.cleaned_data['title']
            
            clean = re.sub(r'[^\w\s-]', '', title)
            clean = clean.replace(' ', '_')
            obj.slug = slugify(clean, allow_unicode=True)

            obj.visibility_status = 'under_review'
            obj.created_at = timezone.now()
            obj.updated_at = timezone.now()

            obj.save()
            return redirect(redirect_view, slug=obj.slug)
    else:
        form = FormClass()

    return render(request, template, {'form': form})



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
            

def normalize_text(text):
    if not text:
        return ""
    text = re.sub(r'[^\w\sء-ي]', '', text)
    text = text.strip().lower()
    return text


@csrf_exempt
def store_comment(request):
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', '/'))

    try:
        referer = request.META.get('HTTP_REFERER', '')
        if referer:
            path_parts = unquote(referer).split('/')
            page_title = path_parts[-2] if path_parts[-1] == '' else path_parts[-1]
            page_title = page_title.replace('-', ' ').replace('_', ' ')
            page_title = ' '.join(word.capitalize() for word in page_title.split())
        else:
            page_title = request.POST.get('page_title', 'صفحة بدون عنوان').strip()

        if request.user.is_authenticated:
            author_name = f"{request.user.first_name} {request.user.last_name}".strip()
            author_email = request.user.email
        else:
            author_name = request.POST.get('author_name', '').strip()
            author_email = request.POST.get('author_email', '').strip()

        cmt_subject = request.POST.get('cmt_subject', '').strip()

        if not cmt_subject:
            raise ValidationError("نص التعليق مطلوب")
        if not author_name:
            raise ValidationError("اسم المؤلف مطلوب")

        comment_data = {
            'page_title': escape(page_title),
            'author_name': escape(author_name),
            'author_email': escape(author_email),
            'cmt_subject': escape(cmt_subject),
            'visibility_status': 'under_review'
        }

        new_comment = Comments(**comment_data)

        if request.user.is_authenticated and hasattr(comments, 'user'):
            new_comment.user = request.user

        new_comment.full_clean()
        new_comment.save()

        logger.info(f"تم إضافة تعليق جديد ID: {new_comment.cmt_id} للصفحة: {page_title}")

        messages.success(request, "تم إضافة تعليقك بنجاح! سيظهر بعد المراجعة")
        return redirect(request.META.get('HTTP_REFERER', '/') + '#comments')

    except ValidationError as e:
        logger.warning(f"تحقق من صحة فاشل: {e}")
        messages.error(request, str(e))
    except Exception as e:
        logger.error(f"خطأ في إضافة تعليق: {str(e)}", exc_info=True)
        messages.error(request, "حدث خطأ تقني أثناء حفظ التعليق")

    return redirect(request.META.get('HTTP_REFERER', '/') + '#comment-form')


def serve_pdf(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'ebookZone', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else:
        raise Http404("PDF not found")

models = [
    {'model': articles, 'id_column': 'art_id'},
    {'model': books, 'id_column': 'books_id'},
    {'model': exams, 'id_column': 'exam_id'},
    {'model': videos, 'id_column': 'vd_id'},
    {'model': cours, 'id_column': 'cours_id'},
]

def store_reaction(request):
    if request.method == 'POST':
        try:
            page_title = request.POST.get('page_title')
            reaction_type = request.POST.get('reaction_type')
            
            ip_or_name = request.META.get('REMOTE_ADDR', '')
            if request.user.is_authenticated:
                ip_or_name = request.user.username
                
            ArticleReaction.objects.create(
                ip_or_name=ip_or_name,
                page_title=page_title,
                reaction_type=reaction_type,
                device_type=request.META.get('HTTP_USER_AGENT', '')[:100],
                liked_at=datetime.now(),
                created_at=datetime.now()
            )
            messages.success(request, 'شكراً لتعبيرك عن رأيك!')
        except Exception as e:
            messages.error(request, 'حدث خطأ أثناء حفظ التفاعل')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def comment_view(request, title=None):
    if not title:
        referer = request.META.get('HTTP_REFERER', '')
        if referer:
            try:
                path_parts = unquote(referer).split('/')
                title = path_parts[-2] if path_parts[-1] == '' else path_parts[-1]
                title = title.replace('-', ' ').replace('_', ' ').strip()
            except Exception as e:
                logger.warning(f"Failed to extract title from URL: {str(e)}")
                title = "صفحة بدون عنوان"
    
    public_comments = comments.objects.filter(
        page_title=title,
        visibility_status='public'
    ).order_by('cmt_id')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                
                if request.user.is_authenticated:
                    comment.user = request.user
                    comment.author_name = f"{request.user.first_name} {request.user.last_name}".strip()
                    comment.author_email = request.user.email
                
                # ضمان تطابق عنوان الصفحة
                comment.page_title = title
                comment.visibility_status = 'under_review'
                
                comment.full_clean()
                comment.save()
                
                messages.success(request, 'تم إرسال تعليقك بنجاح وسيظهر بعد المراجعة')
                return redirect(f"{request.path}#comments-section")
            
            except ValidationError as e:
                logger.warning(f"Validation error in comment: {str(e)}")
                messages.error(request, f"خطأ في البيانات: {str(e)}")
            except Exception as e:
                logger.error(f"Error saving comment: {str(e)}", exc_info=True)
                messages.error(request, 'حدث خطأ غير متوقع أثناء حفظ التعليق')
        else:
            messages.error(request, 'يوجد خطأ في البيانات المدخلة')
    
    initial_data = {'page_title': title}
    
    if request.user.is_authenticated:
        initial_data.update({
            'author_name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'author_email': request.user.email
        })
    
    form = CommentForm(initial=initial_data)
    
    context = {
        'form': form,
        'comments': public_comments,
        'title': title,
        'user': request.user,
        'obj': getattr(request, 'obj', None) 
    }
    
    return render(request, 'tifinar/comments/article_comments.html', context)
