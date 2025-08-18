from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tifinar.models import articles, videos, cours, books, exams

def contents(request):
    # معالجة معلمات البحث والتصفية
    search = request.GET.get("search", "").strip()
    the_type = request.GET.get("the_type", "").strip()
    path = request.path.strip('/')

    # تحديد نوع المحتوى بناء على المسار
    if path == "فيديوهات":
        model = videos
        title = "فيديوهات"
        description = "مجموعة متنوعة من الفيديوهات التعليمية والثقافية"
        template_name = "tifinar/videos.html"
    elif path == "قواميس_بصرية":
        model = cours
        title = "قواميس بصرية"
        description = "قواميس مصورة لتعلم المفردات بلغة تيفيناغ"
        template_name = "tifinar/contents.html"
    elif path == "مقالات":
        model = articles
        title = "مقالات"
        description = "مقالات متنوعة في الثقافة الأمازيغية والعلوم"
        template_name = "tifinar/contents.html"
    elif path == "اختبارات":
        model = exams
        title = "اختبارات"
        description = "اختبارات تفاعلية لتقييم المستوى في اللغة الأمازيغية"
        template_name = "tifinar/contents.html"
    elif path == "مكتبة_تيفيناغ":
        model = books
        title = "مكتبة تيفيناغ"
        description = "مجموعة من الكتب والمراجع التعليمية المجانية"
        template_name = "tifinar/books.html"
    else:
        return render(request, 'tifinar/404.html', status=404)

    # استعلام قاعدة البيانات
    queryset = model.objects.all()

    # تطبيق عوامل التصفية
    if the_type:
        queryset = queryset.filter(the_type__icontains=the_type)

    if search:
        # إنشاء شروط البحث
        search_conditions = (
            Q(title__icontains=search) |
            Q(keywords__icontains=search) |
            Q(the_type__icontains=search) |
            Q(mysubject__icontains=search) |
            Q(mydescription__icontains=search)
        )
        queryset = queryset.filter(search_conditions).annotate(
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
    else:
        queryset = queryset.order_by('-created_at')
        
    # معالجة الصور للمحتوى
    for item in queryset:
        if hasattr(item, 'myimage') and item.myimage:
            item.images = item.myimage.split(',')
        else:
            item.images = []

    # إعداد قائمة أنواع المحتوى للتصفية
    types_list = [
        'الأمازيغية',
        'تربية وتعليم',
        'الثقافة العامة',
        'علوم',
        'القانون وحقوق الإنسان'
    ]

    # التقسيم إلى صفحات
    items_per_page = 11 if path in ["فيديوهات", "مكتبة_تيفيناغ"] else 5
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # إعداد بيانات القالب
    context = {
        'current_url': request.build_absolute_uri(),
        'description': description,
        'title': title,
        'dir': 'rtl',
        'articles': page_obj,
        'page_obj': page_obj,      # هذا ما يحتاجه الـ template
        'types_list': types_list,
        'table_name': model._meta.db_table,
        'paginator': paginator,
        'search_query': search,
        'selected_type': the_type,
    }

    return render(request, template_name, context)