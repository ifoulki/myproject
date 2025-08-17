from django.urls import path
from django.http import Http404
from importlib import import_module
from tifinar.models import articles, videos, cours, books
from django.db import connection

def table_exists(table_name):
    return table_name in connection.introspection.table_names()

CONTENT_TYPES = [
    ('articles', articles, 'tifinar.views.content.articles.article_detail'),
    ('videos', videos, 'tifinar.views.content.videos.video_detail'),
    ('cours', cours, 'tifinar.views.content.cours.cours_detail'),
    ('books', books, 'tifinar.views.content.books.book_detail'),
]

def get_view(view_path):
    try:
        module_path, view_name = view_path.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, view_name)
    except (ImportError, AttributeError) as e:
        print(f"Error importing view {view_path}: {e}")
        return None

def content_router(request, slug):
    for content_type, model, view_path in CONTENT_TYPES:
        try:
            if not table_exists(model._meta.db_table):
                continue
                
            obj = model.objects.filter(slug=slug).first()
            if obj:
                view = get_view(view_path)
                if view:
                    return view(request, slug)
        except Exception as e:
            print(f"Error in {content_type} lookup: {str(e)}")
            continue
    
    raise Http404("المحتوى غير موجود")

urlpatterns = [
    path('<str:slug>/', content_router, name='dynamic_content'),
]