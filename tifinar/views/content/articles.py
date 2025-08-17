from django.shortcuts import render, get_object_or_404
from tifinar.models import articles

def article_detail(request, slug):
    """
    عرض محتوى المقال عند الدخول على الرابط مثل:
    http://127.0.0.1:8000/أربع_طرق_لحفظ_أكبر_عدد_من_المصطلحات_الأمازيغية/
    """
    article = get_object_or_404(articles, slug=slug)
    
    return render(request, 'tifinar/showContent.html', {
        'article': article,
        'title': article.title,
        'content': article.mysubject,  # استخدام الحقل الصحيح
        'description': article.mydescription,
        'image': article.myimage,
        'author': article.author
    })