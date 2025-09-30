from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from tifinar.models import articles, books, exams, videos, cours, comments
from tifinar.myForms.article.create_article_form import ArticleForm
from tifinar.forms import BookForm, ExamForm, VideoForm, CommentForm
from tifinar.myForms.cours.create_cours_form import CoursForm
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
from django.utils import timezone


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

    # جلب التعليقات المرتبطة بالمقال
    content_comments = []
    comment_forms = []

    if content_type == 'articles':
        content_comments = comments.objects.filter(page_title=content.title)
        # إنشاء نماذج لكل تعليق
        for comment in content_comments:
            comment_forms.append(CommentForm(instance=comment))

    if request.method == 'POST':
        # التحقق مما إذا كان الطلب لتعديل مقال أو تعليق
        if 'comment_id' in request.POST:
            # هذا طلب لتعديل تعليق
            comment_id = request.POST.get('comment_id')
            try:
                comment_obj = comments.objects.get(cmt_id=comment_id)
                comment_form = CommentForm(request.POST, instance=comment_obj)
                if comment_form.is_valid():
                    # تحديث حقل updated_at قبل الحفظ
                    comment_obj.updated_at = timezone.now()
                    comment_form.save()
                    messages.success(request, 'تم تحديث التعليق بنجاح')
                    return redirect(request.path)


                else:
                    messages.error(request, 'حدث خطأ في تحديث التعليق')
                    # إضافة أخطاء النموذج للرسائل
                    for field, errors in comment_form.errors.items():
                        for error in errors:
                            messages.error(request, f"{field}: {error}")
            except comments.DoesNotExist:
                messages.error(request, 'التعليق غير موجود')
        else:
            # هذا طلب لتعديل المقال
            form = config['form_class'](request.POST, request.FILES, instance=content)
            if form.is_valid():
                content = form.save(commit=False)
                image_fields = ['myimage', 'autre']
                original_images = {field: getattr(content, field, '') for field in image_fields}

                for field in image_fields:
                    if field in request.FILES and request.FILES[field]:
                        new_files = request.FILES.getlist(field)
                        processed_value = handle_uploaded_images(
                            new_files, original_images[field], content.slug, field.split('_')[-1]
                        )
                        setattr(content, field, processed_value)
                    else:
                        setattr(content, field, original_images[field])

                update_fields = [
                    f.name for f in content._meta.get_fields()
                    if f.concrete and not f.primary_key and not f.many_to_many and not f.one_to_many
                    and f.name not in image_fields
                ]
                content.save(update_fields=update_fields)

                for field in image_fields:
                    if not (field in request.FILES and request.FILES[field]):
                        ModelClass.objects.filter(pk=content.pk).update(**{field: original_images[field]})

                if hasattr(form, 'save_m2m'):
                    form.save_m2m()

                messages.success(request, 'تم تحديث المحتوى بنجاح')
                return redirect(request.path)

    else:
        form = config['form_class'](instance=content)

    # إذا لم تكن هناك نماذج تعليقات، أنشئها
    if not comment_forms and content_type == 'articles':
        for comment in content_comments:
            comment_forms.append(CommentForm(instance=comment))

    context = {
        'title': 'تعديل مقال : '+ content.title,
        'article': content,
        'form': form,
        'content_types': config['types'],
        'comments': zip(content_comments, comment_forms) if content_type == 'articles' else [],
        'comment_count': content_comments.count() if content_type == 'articles' else 0
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
