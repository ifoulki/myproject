from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from tifinar.models import articles
from django.utils import timezone
from django.http import Http404
from django.conf import settings

def article_detail(request, slug):
    # التحقق من وجود المقال مع مراعاة حالة النشر
    try:
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            # للمستخدمين المصرح لهم، عرض جميع المقالات بما فيها غير المنشورة
            article = articles.objects.get(slug=slug)
        else:
            # للزوار العاديين، عرض المقالات المنشورة فقط
            article = articles.objects.get(slug=slug, visibility_status='public')
    except articles.DoesNotExist:
        raise Http404("المقال غير موجود أو غير منشور بعد")
    
    # تسجيل زيارة المقال (إذا أردت تتبع الإحصائيات)
    if hasattr(settings, 'TRACK_VISITS') and settings.TRACK_VISITS:
        try:
            from tifinar.models import ArticleVisit
            ArticleVisit.objects.create(
                article=article,
                user=request.user if request.user.is_authenticated else None,
                ip_address=get_client_ip(request)
            )
        except:
            pass  # تجاهل الأخطاء في تتبع الزيارات
    
    # الحصول على المقال التالي باستخدام art_id
    next_obj = (
        articles.objects.filter(
            art_id__gt=article.art_id, 
            visibility_status='public'
        ).order_by('art_id').first() or
        articles.objects.filter(
            art_id__lt=article.art_id,
            visibility_status='public'
        ).order_by('-art_id').first()
    )

    # المقالات ذات الصلة
    base_query = articles.objects.exclude(slug=slug).filter(visibility_status='public')
    
    if request.user.is_authenticated:
        user = request.user
        query = Q()
        
        # التصفية حسب المستوى التعليمي
        if hasattr(user, 'educational_level') and user.educational_level:
            query |= Q(educational_level=user.educational_level)
        
        # التصفية حسب الجنس
        if hasattr(user, 'gender') and user.gender:
            query |= Q(gender=user.gender) | Q(gender='all')
        else:
            query |= Q(gender='all')
        
        # التصفية حسب العمر
        if hasattr(user, 'Date_de_naissance') and user.Date_de_naissance:
            try:
                age = timezone.now().year - user.Date_de_naissance.year
                query |= Q(min_age__lte=age, max_age__gte=age)
            except:
                pass  # تجاهل أخطاء حساب العمر
        
        # إذا كان هناك استعلام، استخدمه، وإلا استخدم الاستعلام الافتراضي
        if query:
            related_articles = base_query.filter(query)
        else:
            related_articles = base_query.filter(
                Q(the_type__in=['أصناف أخرى', 'الثقافة العامة', 'without_board', 'عام', 'متنوع']) |
                Q(the_type__isnull=True)
            )
    else:
        # للزوار غير المسجلين
        related_articles = base_query.filter(
            Q(the_type__in=['أصناف أخرى', 'الثقافة العامة', 'without_board', 'عام', 'متنوع']) |
            Q(the_type__isnull=True) |
            Q(gender='all')
        ).filter(
            Q(min_age__lte=18, max_age__gte=18)  # افتراضي لعمر 18 للزوار
        )

    # أخذ 6 مقالات عشوائية
    related_articles = list(related_articles.order_by('?')[:6])

    # إعداد السياق
    context = {
        'article': article,  # الكائن الكامل للمقال
        'title': article.title,
        'subject': article.mysubject,
        'description': article.mydescription,
        'myimage': article.myimage,
        'folder': "articles",
        'author': article.author,
        'autre': article.autre,
        'dir': article.dir,  # أضفت حقل الاتجاه
        'next_obj': next_obj,
        'related_articles': related_articles,
        'updated_at': article.updated_at,
        'keywords': article.keywords,  # أضفت الكلمات المفتاحية
    }
    
    return render(request, 'tifinar/showArticle.html', context)


# دالة مساعدة للحصول على IP العميل
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
