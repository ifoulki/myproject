from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tifinar.models import articles, videos, cours, books, exams

def index_eddit(request):
    # معالجة معلمات البحث والتصفية
    search = request.GET.get("search", "").strip()
    the_type = request.GET.get("the_type", "").strip()
    path = request.path.strip('/')

    # تحديد نوع المحتوى بناء على المسار
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
        'types_list': types_list,
        'table_name': model._meta.db_table,
        'paginator': paginator,
        'search_query': search,
        'selected_type': the_type,
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