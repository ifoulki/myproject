from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.db import models
from .models import articles, books, exams, videos, cours, comments, ArticleReaction, VisitorsIp,AuthUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Case, When, IntegerField, Sum
from .forms import CommentForm, ArticleForm, BookForm, MsgForm, ExamForm, CoursForm, VideoForm,UserEditForm
from django.contrib import messages
from django.http import FileResponse, Http404, JsonResponse
from django.utils.safestring import mark_safe
import os
from django.conf import settings
from urllib.parse import unquote
from django.utils import timezone
import logging
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.text import slugify
import re

from datetime import timedelta
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib as mpl
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404

@login_required
def show_user(request, user_id=None):
    if user_id:
        user = get_object_or_404(AuthUser, pk=user_id)
    else:
        user = request.user
    
    context = {
        'user': user,
        'user_full_name': user.get_full_name(),
        'user_role': user.get_role_display(),
        'educational_level': user.get_educational_level_display(),
    }
    return render(request, 'tifinar/auth/show_user.html', context)

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

plt.rcParams['font.family'] = 'Arial'  # أو استخدام خط عربي مثل 'Traditional Arabic'
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

def dashboard(request):
    # إعداد العناوين العربية
    titles = {
        'ip_title': reshape_arabic('عدد الزيارات لكل IP'),
        'device_title': reshape_arabic('نسبة الزيارات حسب نوع الجهاز'),
        'daily_title': reshape_arabic('الزيارات خلال آخر 7 أيام'),
        'page_title': reshape_arabic('عدد الزيارات لكل صفحة'),
        'y_label': reshape_arabic('عدد الزيارات'),
        'x_label_ip': reshape_arabic('عنوان IP'),
        'x_label_date': reshape_arabic('التاريخ'),
        'x_label_page': reshape_arabic('الصفحة'),
    }

    ip_stats = VisitorsIp.objects.values('ip').annotate(
        total_visits=Sum('number_of_visits')
    ).order_by('-total_visits')[:10]
    
    df_ip = pd.DataFrame(list(ip_stats))
    fig_ip, ax_ip = plt.subplots(figsize=(10, 6))
    
    df_ip['ip'] = df_ip['ip'].apply(lambda x: reshape_arabic(x) if any('\u0600' <= c <= '\u06FF' for c in str(x)) else x)
    
    df_ip.plot.bar(x='ip', y='total_visits', ax=ax_ip, color='purple', alpha=0.6)
    ax_ip.set_title(titles['ip_title'], fontsize=14)
    ax_ip.set_ylabel(titles['y_label'])
    ax_ip.set_xlabel(titles['x_label_ip'])
    plt.xticks(rotation=45)
    ip_chart = generate_chart_image(fig_ip)

    device_stats = VisitorsIp.objects.values('device_type').annotate(
        total_visits=Sum('number_of_visits')
    ).order_by('-total_visits')
    
    df_device = pd.DataFrame(list(device_stats))
    fig_device, ax_device = plt.subplots(figsize=(10, 6))
    
    df_device['device_type'] = df_device['device_type'].fillna(reshape_arabic('غير معروف'))
    df_device['device_type'] = df_device['device_type'].apply(lambda x: reshape_arabic(x) if any('\u0600' <= c <= '\u06FF' for c in str(x)) else x)
    
    df_device.plot.pie(
        y='total_visits', 
        labels=df_device['device_type'],
        autopct='%1.1f%%',
        ax=ax_device,
        colors=['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0'],
        textprops={'fontsize': 12}
    )
    ax_device.set_title(titles['device_title'], fontsize=14)
    device_chart = generate_chart_image(fig_device)

    # إحصائيات الزيارات اليومية
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_stats = VisitorsIp.objects.filter(
        visit_timestamp__gte=seven_days_ago
    ).extra({'date': "DATE(visit_timestamp)"}).values('date').annotate(
        daily_visits=Sum('number_of_visits')
    ).order_by('date')
    
    df_daily = pd.DataFrame(list(daily_stats))
    
    if df_daily.empty:
        df_daily = pd.DataFrame({
            'date': pd.date_range(end=timezone.now(), periods=7).date,
            'daily_visits': [0] * 7
        })
    
    fig_daily, ax_daily = plt.subplots(figsize=(10, 6))
    df_daily.plot.line(x='date', y='daily_visits', ax=ax_daily, marker='o', color='teal', alpha=0.6)
    ax_daily.set_title(titles['daily_title'], fontsize=14)
    ax_daily.set_ylabel(titles['y_label'])
    ax_daily.set_xlabel(titles['x_label_date'])
    plt.xticks(rotation=45)
    daily_chart = generate_chart_image(fig_daily)

    pages = [
        {'page': reshape_arabic('الصفحة الرئيسية'), 'visits': 120},
        {'page': reshape_arabic('اتصل بنا'), 'visits': 80},
        {'page': reshape_arabic('من نحن'), 'visits': 50}
    ]
    
    df_page = pd.DataFrame(pages)
    fig_page, ax_page = plt.subplots(figsize=(10, 6))
    df_page.plot.bar(x='page', y='visits', ax=ax_page, color='blue', alpha=0.6)
    ax_page.set_title(titles['page_title'], fontsize=14)
    ax_page.set_ylabel(titles['y_label'])
    ax_page.set_xlabel(titles['x_label_page'])
    plt.xticks(rotation=45)
    page_chart = generate_chart_image(fig_page)

    context = {
        'ip_chart': ip_chart,
        'device_chart': device_chart,
        'daily_chart': daily_chart,
        'page_chart': page_chart,
    }
        
    return render(request, 'tifinar/auth/dashboard.html', context)

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
            

def send_message(request):
    if request.method == 'POST':

        form = MsgForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)

            if not msg.author_id:
                msg.author_id = '0'
            if not msg.recipient:
                msg.recipient = '1'
            if not msg.author_img:
                msg.author_img = ''
            
            msg.save()

            messages.success(request, 'تم إرسال رسالتك بنجاح!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'حدث خطأ أثناء إرسال الرسالة. تأكد من صحة البيانات.')

    else:
        form = MsgForm()

    return render(request, 'tifinar/send_message.html', {'form': form})

def rps_game(request):
    return render(request, 'tifinar/game.html')

def normalize_text(text):
    if not text:
        return ""
    text = re.sub(r'[^\w\sء-ي]', '', text)
    text = text.strip().lower()
    return text

def showContent(request, slug):
    found_obj = None
    model_cls = None
    id_col = None
    folder = None

    for m in models:
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
    next_obj = None
    if current_id is not None:
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

        related_articles = base_query.filter(education_query) if education_query else base_query.none()
    else:
        related_articles = base_query.filter(
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

    if not related_articles:
        # بناء استعلام آمن مع التحقق من وجود القيم
        query = Q()
        if found_obj.title:
            query |= Q(title__icontains=found_obj.title)
        if found_obj.the_type:
            query |= Q(the_type__icontains=found_obj.the_type)
        if found_obj.keywords:
            query |= Q(keywords__icontains=found_obj.keywords)
        
        if query:
            similar_query = base_query.filter(query).distinct()
            related_articles = list(similar_query)

    all_comments = comments.objects.filter(visibility_status='public')
    
    if found_obj.title:
        try:
            all_comments = comments.objects.filter(
                visibility_status='public'
            ).only('page_title', 'cmt_subject', 'author_name')
            
            target_title = found_obj.title.lower().strip()
            comments_list = [
                comment for comment in all_comments
                if comment.page_title and 
                comment.page_title.lower().strip() == target_title
            ]
        except Exception as e:
            logger.error(f"Error fetching comments: {str(e)}")
            comments_list = []

    context = {
        'current_url': request.build_absolute_uri(),
        'title': found_obj.title,
        'image': found_obj.myimage,
        'description': found_obj.mydescription,
        'author': found_obj.author,
        'obj': found_obj,
        'folder': folder,
        'next_obj': next_obj,
        'related_articles': related_articles or [],
        'comments': comments_list,
        'url': request.build_absolute_uri(),
        'autres_list': found_obj.autre.split(',') if found_obj.autre else [],
    }

    return render(request, 'tifinar/showContent.html', context)


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

def contents(request, content_type):

    search = request.GET.get("search", "").strip()
    the_type = request.GET.get("the_type", "").strip()

    path = request.path.strip('/')
    if path == "فيديوهات":
        model = videos
        title = "فيديوهات"
        description = "مجلة تيفيناغ الثقافية تضم سلسلات كثيرة ومتنوعة لفيديوهات ثقافية، تربوية وتعليمية ... إلخ، يمكتكم متابعتها والاستفادة منها مجانا"
    elif path == "قواميس_بصرية":
        model = cours
        title = "قواميس بصرية"
        description = "موقع تيفيناغ يقدم لكم مجموعة من القواميس البصرية لأجل مساعدة الراغبين في إغناء رصيدهم اللغوي، بطريقة سهلة ومبسطة بالصوت والصورة"
    elif path == "مقالات":
        model = articles
        title = "مقالات"
        description = "مجلة تيفيناغ تقترح عليكم مجموعة من المقالات في مختلف المجالات العلمية والثقافية والتربوية، ويمكن للزوار أيضا إغناء الموقع بمشاركاتهم في النشر عبر مشاركة مواضيغهم معنا"
    elif path == "اختبارات":
        model = exams
        title = "اختبارات"
        description = "موقع مجلة تيفيناغ يعد منصة رائعة للراغبين في الإستعداد الجيد للإمتحانات، حيث يمكن من خلاله للزوار اجتياز اختبارات تجريبية online  وتظهر لهم النتيجة مباشرة بعد نهاية الاختبار، وذلك يساعدهم على تتبع مستواهم أثناء الاستعداد للإمتحانات"
    elif path == "مكتبة_تيفيناغ":
        model = books
        title = "مكتبة تيفيناغ"
        description='في مكتبة تيفيناغ يمكن تحميل كتب متنوعة مجانا، بما فيها الكتب المدرسية ونماذج امتحانات وفروض لتدريب التلاميذ وإعدادهم للاختبارات المدرسية'
    else:
        return showContent(request, slug)

    queryset = model.objects.all()

    if the_type:
        queryset = queryset.filter(the_type__icontains=the_type)

    if search:
        search_conditions = (
            Q(title__icontains=search) |
            Q(keywords__icontains=search) |
            Q(the_type__icontains=search) |
            Q(mysubject__icontains=search) |
            Q(mydescription__icontains=search)
        )
        queryset = queryset.filter(search_conditions)

        queryset = queryset.annotate(
            relevance=Case(
                When(title__icontains=search, then=1),
                When(keywords__icontains=search, then=2),
                When(the_type__icontains=search, then=3),
                When(mysubject__icontains=search, then=4),
                When(mydescription__icontains=search, then=5),
                default=6,
                output_field=IntegerField(),
            )
        ).order_by('relevance')

    # معالجة الصور
    for article in queryset:
        if article.myimage:
            images = article.myimage.split(',')
            article.images = list(reversed(images))            
        else:
            article.images = []

    types_list = ['الأمازيغية', 'تربية وتعليم', 'الثقافة العامة', 'علوم', 'القانون وحقوق الإنسان']
   
    page = request.GET.get('page', 1)  # رقم الصفحة من الرابط

    if model == videos or model == books:
        paginator = Paginator(queryset, 11)  # 10 عناصر في الصفحة الواحدة
    else :
        paginator = Paginator(queryset, 5)  # 10 عناصر في الصفحة الواحدة

    try:
        articles_page = paginator.page(page)
    except PageNotAnInteger:
        # إذا كان رقم الصفحة غير صحيح، أرجع الصفحة الأولى
        articles_page = paginator.page(1)
    except EmptyPage:
        # إذا كانت الصفحة أكبر من عدد الصفحات، أرجع آخر صفحة
        articles_page = paginator.page(paginator.num_pages)

    current_url = request.build_absolute_uri()

    context = {
        'current_url' : current_url,
        'description': description,
        "objects": {'articles': articles_page},
        "title": title,
        "dir": queryset[0].dir if queryset.exists() and hasattr(queryset[0], 'dir') else "ltr",
        "articles": articles_page,
        "types_list": types_list,
        "table_name" : queryset.model._meta.db_table,
        "paginator": paginator,  # إرسال paginator للتمكن من الوصول للمعلومات بالتمبلت
        "page_obj": articles_page,
    }
    if model == videos:
        return render(request, "tifinar/videos.html", context)
    elif model == books:
        return render(request, "tifinar/books.html", context)
    else:
        return render(request, "tifinar/contents.html", context)
    

def index_edit(request):
    
    search = request.GET.get("search", "").strip()
    the_type = request.GET.get("the_type", "").strip()
    
    path = request.path.strip('/')
    if path == "videos_edit":
        model = videos
        title = "فيديوهات"
        description = "مجلة تيفيناغ الثقافية تضم سلسلات كثيرة ومتنوعة لفيديوهات ثقافية، تربوية وتعليمية ... إلخ، يمكتكم متابعتها والاستفادة منها مجانا"
    elif path == "cours_edit":
        model = cours
        title = "قواميس بصرية"
        description = "موقع تيفيناغ يقدم لكم مجموعة من القواميس البصرية لأجل مساعدة الراغبين في إغناء رصيدهم اللغوي، بطريقة سهلة ومبسطة بالصوت والصورة"
    elif path == "articles_edit":
        model = articles
        title = "مقالات"
        description = "مجلة تيفيناغ تقترح عليكم مجموعة من المقالات في مختلف المجالات العلمية والثقافية والتربوية، ويمكن للزوار أيضا إغناء الموقع بمشاركاتهم في النشر عبر مشاركة مواضيغهم معنا"
    elif path == "exams_edit":
        model = exams
        title = "اختبارات"
        description = "موقع مجلة تيفيناغ يعد منصة رائعة للراغبين في الإستعداد الجيد للإمتحانات، حيث يمكن من خلاله للزوار اجتياز اختبارات تجريبية online  وتظهر لهم النتيجة مباشرة بعد نهاية الاختبار، وذلك يساعدهم على تتبع مستواهم أثناء الاستعداد للإمتحانات"
    elif path == "books_edit":
        model = books
        title = "مكتبة تيفيناغ"
        description='في مكتبة تيفيناغ يمكن تحميل كتب متنوعة مجانا، بما فيها الكتب المدرسية ونماذج امتحانات وفروض لتدريب التلاميذ وإعدادهم للاختبارات المدرسية'
    else:
        return showContent(request, slug)

    queryset = model.objects.all()
    
    if the_type:
        queryset = queryset.filter(the_type__icontains=the_type)

    if search:
        search_conditions = (
            Q(title__icontains=search) |
            Q(keywords__icontains=search) |
            Q(the_type__icontains=search) |
            Q(mysubject__icontains=search) |
            Q(mydescription__icontains=search)
        )
        queryset = queryset.filter(search_conditions)

        queryset = queryset.annotate(
            relevance=Case(
                When(title__icontains=search, then=1),
                When(keywords__icontains=search, then=2),
                When(the_type__icontains=search, then=3),
                When(mysubject__icontains=search, then=4),
                When(mydescription__icontains=search, then=5),
                default=6,
                output_field=IntegerField(),
            )
        ).order_by('relevance')
    
     # معالجة الصور
    for article in queryset:
        if article.myimage:
            images = article.myimage.split(',')
            article.images = list(reversed(images))            
        else:
            article.images = []

    types_list = ['الأمازيغية', 'تربية وتعليم', 'الثقافة العامة', 'علوم', 'القانون وحقوق الإنسان']

    page = request.GET.get('page', 1)  # رقم الصفحة من الرابط

    if model == videos or model == books:
        paginator = Paginator(queryset, 11)  # 10 عناصر في الصفحة الواحدة
    else :
        paginator = Paginator(queryset, 5)  # 10 عناصر في الصفحة الواحدة

    try:
        articles_page = paginator.page(page)
    except PageNotAnInteger:
        articles_page = paginator.page(1)
    except EmptyPage:
        articles_page = paginator.page(paginator.num_pages)

    current_url = request.build_absolute_uri()

    context = {
        'current_url' : current_url,
        'description': description,
        "objects": {'articles': articles_page},
        "title": title,
        "dir": queryset[0].dir if queryset.exists() and hasattr(queryset[0], 'dir') else "ltr",
        "articles": articles_page,
        "types_list": types_list,
        "table_name" : queryset.model._meta.db_table,
        "paginator": paginator,  # إرسال paginator للتمكن من الوصول للمعلومات بالتمبلت
        "page_obj": articles_page,
    }
    
    if model == videos:
        return render(request, "tifinar/auth/videos/index_videos.html", context)
    elif model == books:
        return render(request, "tifinar/auth/books/index_books.html", context)
    elif model == articles:
        return render(request, "tifinar/auth/articles/index_articles.html", context)
    elif model == exams:
        return render(request, "tifinar/auth/exams/index_exams.html", context)
    elif model == cours:
        return render(request, "tifinar/auth/cours/index_cours.html", context)
    else:
        return 0
