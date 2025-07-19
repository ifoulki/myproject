from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import models
from .models import articles, Books, Exams, Videos, Cours
from django.db.models import Q, Case, When, IntegerField
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import Comments
from django.contrib import messages
from .models import ArticleReaction
from django.http import Http404

# تعريف قائمة الموديلات مع أسماء أعمدة المفتاح الأساسي
models = [
    {'model': articles, 'id_column': 'art_id'},
    {'model': Books, 'id_column': 'books_id'},
    {'model': Exams, 'id_column': 'exam_id'},
    {'model': Videos, 'id_column': 'vd_id'},
    {'model': Cours, 'id_column': 'cours_id'},
]

def showContent(request, slug):
    found_obj = None
    next_obj = None
    folder = None

    for m in models:
        model_cls = m['model']
        id_col = m['id_column']

        try:
            found_obj = model_cls.objects.get(slug=slug)
            folder = found_obj._meta.db_table
            next_obj = model_cls.objects.filter(**{f"{id_col}__gt": getattr(found_obj, id_col)}).order_by(id_col).first()
            break
        except model_cls.DoesNotExist:
            continue

    if not found_obj:
        raise Http404("المحتوى غير موجود")

    # هنا نتحقق من أن found_obj ليس None قبل التفكيك
    autres_list = found_obj.autre.split(',') if (found_obj and found_obj.autre) else []

    context = {
        'obj': found_obj,
        'folder': folder,
        'next_obj': next_obj,
        'url': request.build_absolute_uri(),
        'autres_list': autres_list,
    }

    return render(request, 'tifinar/showContent.html', context)


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

def comment_view(request, title):
    comments = Comments.objects.filter(
        page_title=title,
        visibility_status='visible'
    ).order_by('-created_at')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.user = request.user
                comment.author_name = f"{request.user.first_name} {request.user.last_name}"
                comment.author_email = request.user.email
            comment.visibility_status = 'visible'
            comment.save()
            return redirect(request.path)
    else:
        initial_data = {'page_title': title}
        if request.user.is_authenticated:
            initial_data.update({
                'author_name': f"{request.user.first_name} {request.user.last_name}",
                'author_email': request.user.email
            })
        form = CommentForm(initial=initial_data)
    
    return render(request, 'tifinar/comments/article_comments.html', {
        'form': form,
        'comments': comments,
        'title': title,
        'user': request.user
    })

def contents(request):
    search = request.GET.get("search", "").strip()
    the_type = request.GET.get("the_type", "").strip()

    queryset = articles.objects.all()

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

    context = {
        'objects': {
        'articles': article},
        "title": "المقالات",
        "slug": "ما_معنى_تيفيناغ",
        "dir": "rtl",
        "articles": queryset,
        "types_list": types_list,
        "table_name" : queryset.model._meta.db_table
    }

    return render(request, "tifinar/contents.html", context)
