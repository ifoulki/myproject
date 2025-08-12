from django.http import JsonResponse
from .models import (
    articles, 
    books, 
    exams, 
    videos, 
    cours
)

def content_detail(request, slug):
    """دالة لتفاصيل المحتوى عبر API"""
    try:
        # البحث في جميع النماذج
        content = None
        models_to_search = [articles, books, exams, videos, cours]
        
        for model in models_to_search:
            try:
                content = model.objects.get(slug=slug)
                break
            except model.DoesNotExist:
                continue
        
        if content:
            return JsonResponse({
                'title': getattr(content, 'title', 'No title'),
                'content': getattr(content, 'content', ''),
                'type': content.__class__.__name__.lower()
            })
        return JsonResponse({'error': 'Content not found'}, status=404)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)