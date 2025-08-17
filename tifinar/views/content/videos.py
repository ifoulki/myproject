from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from tifinar.models import videos
from django.utils import timezone

def video_detail(request, slug):
    video = get_object_or_404(videos, slug=slug)
    
    # تصحيح استعلام المقال التالي
    next_obj = (
        videos.objects.filter(vd_id__gt=video.vd_id).order_by('vd_id').first() or
        videos.objects.filter(vd_id__lt=video.vd_id).order_by('-vd_id').first()  # تصحيح: إضافة - للترتيب التنازلي
    )

    base_query = videos.objects.exclude(slug=slug)
    
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
        
        related_videos = base_query.filter(query) if query else base_query.none()
    else:
        # تصحيح بناء استعلام Q
        related_videos = base_query.filter(
            Q(the_type__in=[
                'أصناف أخرى',
                'الثقافة العامة',
                'without_board',
                'عام',
                'متنوع',
                'قصص و روايات',
                'قصائد شعرية',
                'مجلات',
                'لقواميس اللغوية - Dictionaries',
                'أديان',
                'فلسفة',
                'الأمازيغية',
                'العربية',
                'الفرنسية',
                'الإنجليزية',
                'علوم الحاسوب',
                'رياضيات',
                'الكيمياء',
                'الفزياء',
                'علوم الحياة والأرض',
                'صحة وحياة',
                'حقوق الإنسان',
                'تربية وتعليم'
            ]) |
            Q(the_type__isnull=True)
        )

    related_videos = list(related_videos.order_by('?')[:6])

    context = {
        'video': video,
        'title': video.title,
        'subject': video.mysubject,
        'description': video.mydescription,
        'myimage': video.myimage,
        'folder': "videos",
        'author': video.author,
        'autre': video.autre,
        'next_obj': next_obj,
        'related_articles': related_videos,
        'updated_at': video.updated_at,
    }
    
    return render(request, 'tifinar/showContent.html', context)