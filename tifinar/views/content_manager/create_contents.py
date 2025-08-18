from django.shortcuts import render, redirect
from tifinar.models import articles, books, exams, videos, cours
from tifinar.forms import ArticleForm, BookForm, ExamForm, CoursForm, VideoForm
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

from django.utils.text import slugify
import re
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib as mpl


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

