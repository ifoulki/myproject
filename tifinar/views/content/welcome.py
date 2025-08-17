from django.shortcuts import render
from django.utils import timezone
from tifinar.models import myadmin, books, articles, videos

def welcome(request):
    """
    Display the main welcome page with content and ads
    """
    content = {
        'title': "مجلة تيفيناغ - tifinar.net",
        'page': "مجلة تيفيناغ هي مجلة إلكترونية تهتم بنشر المعرفة العلمية والثقافية وتبسيط العلوم، كما تقدم دروس رائعة لمساعدة التلاميذ والطلاب في دراستهم",
        'image': "education.webp",
        'author': 'حميد بعلوان',
        'date': timezone.now().date(),
        'description': "مجلة تيفيناغ هي مجلة إلكترونية تهتم بنشر المعرفة العلمية والثقافية وتبسيط العلوم، كما تقدم دروس رائعة لمساعدة التلاميذ والطلاب في دراستهم",
        'url': request.build_absolute_uri('/'),
        'folder': "assets",
    }
    
    try:
        admin_settings = myadmin.objects.first()
        if admin_settings:
            content['ads'] = admin_settings.ads or ""  
            content['aside_ads'] = admin_settings.aside_ads or "" 
            content['meta_title'] = admin_settings.meta_title or content['title']
            content['meta_description'] = admin_settings.meta_description or content['description']
        else:
            content['ads'] = ""
            content['aside_ads'] = ""
    except Exception as e:
        print(f"Error loading admin settings: {e}")
        content['ads'] = ""
        content['aside_ads'] = ""
    
    try:
        content['books'] = books.objects.order_by('?')[:4]
        content['articles'] = articles.objects.order_by('?')[:5] 
        content['videos'] = videos.objects.filter(
            the_type__contains='أصناف أخرى'
        ).order_by('?')[:5] 
    except Exception as e:
        print(f"Error loading content: {e}")
        content['books'] = []
        content['articles'] = []
        content['videos'] = []
    
    return render(request, 'tifinar/index.html', content)