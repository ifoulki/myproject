from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from tifinar.models import cours
from django.utils import timezone

def cours_detail(request, slug):
    article = get_object_or_404(cours, slug=slug)
    
    # الحصول على المقال التالي باستخدام art_id بدلاً من id
    next_obj = (
        cours.objects.filter(cours_id__gt=article.cours_id).order_by('cours_id').first() or
        cours.objects.filter(cours_id__lt=article.cours_id).order_by('-cours_id').first()
    )

    # المقالات ذات الصلة مع مراعاة المستوى التعليمي والعمر (إذا كان المستخدم مسجل الدخول)
    base_query = cours.objects.exclude(slug=slug)
    
    if request.user.is_authenticated:
        user = request.user
        query = Q()
        
        if hasattr(user, 'educational_level'):
            query |= Q(educational_level=user.educational_level) | Q(educational_level='unknown')
        
        if hasattr(user, 'gender'):
            query |= Q(gender=user.gender) | Q(gender='unknown')
        
        if hasattr(user, 'Date_de_naissance') and user.Date_de_naissance:
            age = timezone.now().year - user.Date_de_naissance.year
            query |= Q(min_age__lte=age, max_age__gte=age)
        
        related_articles = base_query.filter(query) if query else base_query.none()
    else:
        related_articles = base_query.filter(
            Q(the_type__in=['أصناف أخرى', 'الثقافة العامة', 'without_board', 'عام', 'متنوع']) |
            Q(the_type__isnull=True)
        )

    related_articles = list(related_articles.order_by('?')[:6])

    context = {
        'article': article,
        'title': article.title,
        'subject': article.mysubject,
        'description': article.mydescription,
        'myimage': article.myimage,
        'folder': "articles",
        'author': article.author,
        'autre': article.autre,
        'next_obj': next_obj,
        'related_articles': related_articles,
        'updated_at': article.updated_at,
    }
    
    return render(request, 'tifinar/showContent.html', context)
