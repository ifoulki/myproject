from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import models
from .models import articles

def contents(request):
    search = request.GET.get("search", "")
    the_type = request.GET.get("the_type", "")
    
    queryset = articles.objects.all()

    if search:
        queryset = queryset.filter(title__icontains=search)
    
    if the_type:
        queryset = queryset.filter(type=the_type)

    # معالجة الصور لكل مقال
    for article in queryset:
        if article.myimage:
            images = article.myimage.split(',')
            article.images = list(reversed(images))
        else:
            article.images = []

    # لائحة الأنواع بشكل ثابت
    types = ['الأمازيغية', 'تربية وتعليم', 'الثقافة العامة', 'علوم', 'القانون وحقوق الإنسان']

    context = {
        "title": "المقالات",
        "slug": "ما_معنى_تيفيناغ",  # قيمة مؤقتة
        "dir": "rtl",
        "articles": queryset,
        "types": types,  # تم إضافتها هنا
        "table_name" : queryset.model._meta.db_table
    }
    return render(request, "tifinar/contents.html", context)

def showContent(request, slug):
    article = get_object_or_404(articles, slug=slug)
    context = {"articles": article}
    return render(request, "tifinar/showContent.html", context)

