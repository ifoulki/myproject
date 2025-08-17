from django.urls import path
from django.http import Http404
from importlib import import_module
from django.db import connection
from tifinar.models import articles, videos, cours, books, exams,Visitors,VisitorsIp
from tifinar.views.content.content import contents
from tifinar.views.dashboard.dashboard import dashboard_view
from tifinar.views.content.eddit_index import index_eddit

def table_exists(table_name):
    """للتحقق من وجود الجدول في قاعدة البيانات"""
    return table_name in connection.introspection.table_names()

# تعريف أنواع المحتوى المتاحة في النظام
CONTENT_TYPES = [
    ('articles', articles, 'tifinar.views.content.articles.article_detail'),
    ('videos', videos, 'tifinar.views.content.videos.video_detail'),
    ('cours', cours, 'tifinar.views.content.cours.cours_detail'),
    ('books', books, 'tifinar.views.content.books.book_detail'),
    ('exams', exams, 'tifinar.views.content.exams.exam_detail'),
    ('visitors', Visitors, 'tifinar.views.dashboard.dashboard.dashboard_view'),
]

def get_view(view_path):
    """لتحميل دوال العرض الديناميكي"""
    try:
        module_path, view_name = view_path.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, view_name)
    except (ImportError, AttributeError) as e:
        print(f"خطأ في تحميل العرض: {e}")
        return None

def content_router(request, slug):
    """موجه المحتوى الديناميكي"""
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
            print(f"خطأ في البحث عن {content_type}: {str(e)}")
            continue
    
    raise Http404("المحتوى غير موجود")

# مسارات التطبيق
urlpatterns = [
    # الصفحات الرئيسية
    path('مقالات/', contents, name='articles'),
    path('اختبارات/', contents, name='exams'),
    path('قواميس_بصرية/', contents, name='visual_dicts'),
    path('فيديوهات/', contents, name='videos'),
    path('مكتبة_تيفيناغ/', contents, name='books'),
    path('videos_edit/', index_eddit, name='videos_edit'),
    path('cours_edit/', index_eddit, name='cours_edit'),
    path('articles_edit/', index_eddit, name='articles_edit'),
    path('books_edit/', index_eddit, name='books_edit'),
    path('exams_edit/', index_eddit, name='exams_edit'),
    path('adm/dashboard/', dashboard_view, name='dashboard'),

    # المحتوى الديناميكي (يجب أن يكون آخر مسار)
    path('<str:slug>/', content_router, name='dynamic_content'),
]