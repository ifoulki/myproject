from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Case, When, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tifinar.models import articles, videos, cours, books, exams
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings  # أضف هذا
import os
from django.contrib import messages
from django.http import HttpResponseForbidden

def index_eddit(request):
    # معالجة معلمات البحث والتصفية
    search = request.GET.get("search", "").strip()
    the_type = request.GET.get("the_type", "").strip()
    path = request.path.strip('/')

    # تحديد نوع المحتوى بناء على المسار
    if path == "videos_edit":
        model = videos
        title = "فيديوهات"
        order_field = "-vd_id"  # استخدام الحقل الصحيح للترتيب
        description = "مجلة تيفيناغ الثقافية تضم سلسلات كثيرة ومتنوعة لفيديوهات ثقافية، تربوية وتعليمية ... إلخ، يمكتكم متابعتها والاستفادة منها مجانا"
    elif path == "cours_edit":
        model = cours
        title = "قواميس بصرية"  
        order_field = "-cours_id"  # استخدام الحقل الصحيح للترتيب
        description = "موقع تيفيناغ يقدم لكم مجموعة من القواميس البصرية لأجل مساعدة الراغبين في إغناء رصيدهم اللغوي، بطريقة سهلة ومبسطة بالصوت والصورة"
    elif path == "articles_edit":
        model = articles
        title = "مقالات"
        order_field = "-art_id"  # استخدام الحقل الصحيح للترتيب
        description = "مجلة تيفيناغ تقترح عليكم مجموعة من المقالات في مختلف المجالات العلمية والثقافية والتربوية، ويمكن للزوار أيضا إغناء الموقع بمشاركاتهم في النشر عبر مشاركة مواضيغهم معنا"
    elif path == "exams_edit":
        model = exams
        title = "اختبارات"
        order_field = "-exam_id"  # استخدام الحقل الصحيح للترتيب (افتراضي)
        description = "موقع مجلة تيفيناغ يعد منصة رائعة للراغبين في الإستعداد الجيد للإمتحانات، حيث يمكن من خلاله للزوار اجتياز اختبارات تجريبية online  وتظهر لهم النتيجة مباشرة بعد نهاية الاختبار، وذلك يساعدهم على تتبع مستواهم أثناء الاستعداد للإمتحانات"
    elif path == "books_edit":
        model = books
        title = "مكتبة تيفيناغ"
        order_field = "-books_id"  # استخدام الحقل الصحيح للترتيب
        description = 'في مكتبة تيفيناغ يمكن تحميل كتب متنوعة مجانا، بما فيها الكتب المدرسية ونماذج امتحانات وفروض لتدريب التلاميذ وإعدادهم للاختبارات المدرسية'
    else:
        return render(request, 'tifinar/404.html', status=404)

    # استعلام قاعدة البيانات - إضافة شرط استبعاد السجلات ذات slug فارغ
    queryset = model.objects.exclude(slug__isnull=True).exclude(slug__exact='')

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
        # الترتيب حسب الحقل المناسب لكل نموذج
        queryset = queryset.order_by(order_field)

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

    # إضافة Pagination
    paginator = Paginator(queryset, 10)  # 10 عناصر لكل صفحة
    page = request.GET.get('page')
    
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    # إعداد بيانات القالب
    context = {
        'current_url': request.build_absolute_uri(),
        'description': description,
        'title': title,
        'dir': 'rtl',
        'articles': items,
        'types_list': types_list,
        'table_name': model._meta.db_table,
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
    
def delete_content(request, slug):
    if request.method == 'POST':
        try:
            # تحديد النموذج بناءً على المسار
            path = request.path
            if 'articles/delete' in path:
                model = articles
            elif 'videos/delete' in path:
                model = videos
            elif 'cours/delete' in path:
                model = cours
            elif 'books/delete' in path:
                model = books
            elif 'exams/delete' in path:
                model = exams
            else:
                messages.error(request, 'نوع المحتوى غير معروف.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            # استخدام get_object_or_404 مع النموذج المناسب
            item = get_object_or_404(model, slug=slug)
            
            # حذف الملفات المرتبطة بالمحتوى إذا وجدت
            if hasattr(item, 'myimage') and item.myimage:
                image_paths = item.myimage.split(',')
                for path in image_paths:
                    full_path = os.path.join(settings.BASE_DIR, path.strip())
                    if os.path.exists(full_path):
                        os.remove(full_path)
            
            if hasattr(item, 'autre') and item.autre:
                attachment_paths = item.autre.split(',')
                for path in attachment_paths:
                    full_path = os.path.join(settings.BASE_DIR, path.strip())
                    if os.path.exists(full_path):
                        os.remove(full_path)
            
            # حذف المحتوى من قاعدة البيانات
            item.delete()
            
            messages.success(request, 'تم حذف المنشور بنجاح.')
            return redirect(request.META.get('HTTP_REFERER', '/'))            
        except Http404:
            messages.error(request, 'المنشور المطلوب غير موجود.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except Exception as e:
            messages.error(request, f'حدث خطأ أثناء حذف المنشور: {str(e)}')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    return HttpResponseForbidden()