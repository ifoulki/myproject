from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tifinar.models import articles, videos, cours, books, exams

def contents(request):
    # معالجة معلمات البحث والتصفية
    search = request.GET.get("search", "").strip()
    the_type = request.GET.get("the_type", "").strip()
    category = request.GET.get("category", "").strip()
    path = request.path.strip('/')

    # تحديد نوع المحتوى بناء على المسار
    if path == "فيديوهات":
        model = videos
        title = "فيديوهات"
        description = "مجموعة متنوعة من الفيديوهات التعليمية والثقافية"
        template_name = "tifinar/videos.html"
        filter_field = "the_type"
        filter_value = the_type
        types_list = 0
        
    elif path == "قواميس_بصرية":
        model = cours
        title = "قواميس بصرية"
        description = "قواميس مصورة لتعلم المفردات بلغة تيفيناغ"
        template_name = "tifinar/contents.html"
        types_list = [
            ('اللغات', [
                ('english', 'English'),
                ('french', 'Français'),
                ('amazigh', 'الأمازيغية')
            ])
        ]
        filter_field = "category"
        filter_value = the_type
        
    elif path == "مقالات":
        model = articles
        title = "مقالات"
        description = "مقالات متنوعة في الثقافة الأمازيغية والعلوم"
        template_name = "tifinar/contents.html"
        types_list = [ 'الأصناف المتاحة :', [
                        ['تربية وتعليم','تربية وتعليم'],
                        ['الثقافة العامة','الثقافة العامة'],
                        ['القانون وحقوق الإنسان','القانون وحقوق الإنسان'],
                        ['علوم','علوم'],
                        ['الثقافة العامة','الثقافة العامة']
                    ]
        ],
        
        filter_field = "the_type"
        filter_value = the_type
        
    elif path == "اختبارات":
        model = exams
        title = "اختبارات"
        description = "اختبارات تفاعلية لتقييم المستوى في اللغة الأمازيغية"
        template_name = "tifinar/contents.html"
        types_list =  [
            ['الغات :', [
                    ['الأمازيغية', 'تعلم الأمازيغية'],
                    ['العربية', 'تعلم العربية'],
                    ['الفرنسية', 'تعلم الفرنسية'],
                    ['الإنجليزية', 'تعلم الإنجليزية']
                ]
            ],
            ['العلوم :', [
                    ['علوم الحاسوب', 'علوم الحاسوب'],
                    ['رياضيات', 'تعلم الرياضيات'],
                    ['الفيزياء والكيمياء', 'الفيزياء والكيمياء'],
                    ['علوم الحياة والأرض', 'علوم الحياة والأرض']
                ]
            ],
            ['أصناف أخرى :', [
                    ['الثقافة العامة', 'الثقافة العامة'],
                    ['حقوق الإنسان', 'حقوق الإنسان'],
                    ['صحة وحياة', 'صحة وحياة'],
                ]
            ]
        ]
        filter_field = "the_type"
        filter_value = the_type
        
    elif path == "مكتبة_تيفيناغ":
        model = books
        title = "مكتبة تيفيناغ"
        description = "مجموعة من الكتب والمراجع التعليمية المجانية"
        template_name = "tifinar/books.html"
        types_list = 0
        filter_field = "the_type"
        filter_value = the_type
        
    else:
        return render(request, 'tifinar/404.html', status=404)

    # استعلام قاعدة البيانات
    queryset = model.objects.all()

    # تطبيق عوامل التصفية
    if filter_value:
        filter_condition = Q(**{f"{filter_field}__icontains": filter_value})
        queryset = queryset.filter(filter_condition)

    if search:
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
        'page_obj': page_obj,
        'types_list': types_list,
        'table_name': model._meta.db_table,
        'paginator': paginator,
        'search_query': search,
        'selected_type': the_type,
    }

    return render(request, template_name, context)