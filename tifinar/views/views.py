from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, FileResponse
from django.db.models import Q
from django.utils.html import escape
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from urllib.parse import unquote
import os
import re
import logging

from tifinar.models import articles, books, cours, videos, exams

logger = logging.getLogger(__name__)

def normalize_text(text):
    if not text:
        return ""
    text = re.sub(r'[^\w\sء-ي]', '', text)
    text = text.strip().lower()
    return text

content_models = [
    {'model': articles, 'id_column': 'art_id'},
    {'model': books, 'id_column': 'book_id'},
    {'model': exams, 'id_column': 'exam_id'},
    {'model': videos, 'id_column': 'vd_id'},
    {'model': cours, 'id_column': 'cours_id'},
]

def showContent(request, slug):
    found_obj = None
    model_cls = None
    id_col = None
    folder = None

    for m in content_models:
        try:
            found_obj = m['model'].objects.get(slug=slug)
            model_cls = m['model']
            id_col = m['id_column']
            folder = found_obj._meta.db_table
            break
        except m['model'].DoesNotExist:
            continue

    if not found_obj:
        raise Http404("المحتوى غير موجود")

    current_id = getattr(found_obj, id_col)
    next_obj = (
        model_cls.objects.filter(**{f"{id_col}__gt": current_id})
        .order_by(id_col)
        .first() or
        model_cls.objects.filter(**{f"{id_col}__lt": current_id})
        .order_by(f'-{id_col}')
        .first()
    )

    base_query = model_cls.objects.exclude(slug=slug)
    
    if request.user.is_authenticated:
        user = request.user
        user_education = getattr(user, 'educational_level', None)
        user_gender = getattr(user, 'gender', None)
        
        user_age = None
        if hasattr(user, 'Date_de_naissance') and user.Date_de_naissance:
            birth_date = user.Date_de_naissance
            today = timezone.now().date()
            user_age = today.year - birth_date.year - (
                (today.month, today.day) < (birth_date.month, birth_date.day))
        
        education_query = Q()
        if user_education:
            education_query = (
                Q(educational_level=user_education) | 
                Q(educational_level='unknown') |
                Q(educational_level__isnull=True)
            )

        if user_gender:
            education_query &= (
                Q(gender=user_gender) | 
                Q(gender='all') |
                Q(gender__isnull=True)
            )

        if user_age:
            education_query &= (
                Q(min_age__lte=user_age) & 
                Q(max_age__gte=user_age) |
                Q(min_age__isnull=True) |
                Q(max_age__isnull=True)
            )

        related_articles = base_query.filter(education_query)
    else:
        related_articles = base_query.filter(
            Q(educational_level='unknown') | 
            Q(educational_level__isnull=True),
            Q(the_type__in=[
                'أصناف أخرى',
                'الثقافة العامة',
                'without_board',
                'عام',
                'متنوع'
            ]) | Q(the_type__isnull=True)
        )

    related_articles = list(
        related_articles.distinct()
        .order_by('?')
        .only('slug', 'title', 'myimage', 'the_type')[:6]
    )

    context = {
        'obj': found_obj,
        'folder': folder,
        'next_obj': next_obj,
        'related_articles': related_articles or [],
        'autres_list': found_obj.autre.split(',') if found_obj.autre else [],
    }

    return render(request, 'tifinar/showContent.html', context)

def serve_pdf(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'tifinar', 'static', 'tifinar', 'ebookZone', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    else:
        raise Http404("PDF not found")
