from django.urls import path
from django.http import Http404
from importlib import import_module
from django.db import connection
from tifinar.models import articles, videos, cours, books, exams, Visitors, AuthUser
from tifinar.views.content.content import contents
from tifinar.views.dashboard.dashboard import dashboard_view
from tifinar.views.content.eddit_index import index_eddit
from tifinar.views.content.welcome import welcome
from tifinar.views.games.rock_paper_scissors import rps_game
from tifinar.views.audience.msgs import send_message
from tifinar.views.content.cours import show_cours 
from tifinar.views.members.user import show_user 
from tifinar.views.members.members_index import members_index 
from tifinar.views.contacts.contacts_index import contacts_index
from tifinar.views.contacts.create_contact import contact_create
from tifinar.views.members.user import edit_user 
from tifinar.views.members.show_member import member_profile_view, edit_member_profile, delete_member_profile, manage_member_relations, update_profile_image
from tifinar.views.contacts.show_contact import contact_view,edit_contact, delete_contact, manage_contact_relations, update_contact_image
from tifinar.views.content_manager.create_contents import create_content 
from tifinar.views.content_manager.edit_contents import edit_content
from .logout import custom_logout

def table_exists(table_name):
    """للتحقق من وجود الجدول في قاعدة البيانات"""
    return table_name in connection.introspection.table_names()

# تعريف أنواع المحتوى المتاحة في النظام
CONTENT_TYPES = [
    ('articles', articles, 'tifinar.views.content.articles.article_detail'),
    ('videos', videos, 'tifinar.views.content.videos.video_detail'),
    ('cours', cours, 'tifinar.views.content.cours.show_cours'), 
    ('books', books, 'tifinar.views.content.books.book_detail'),
    ('exams', exams, 'tifinar.views.content.exams.exam_detail'),
    ('visitors', Visitors, 'tifinar.views.dashboard.dashboard.dashboard_view'),
    ('user', AuthUser, 'tifinar.views.users.user.show_user'),
    ('edit_user', AuthUser, 'tifinar.views.users.user.edit_user'),
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
    print(f"البحث عن slug: {slug}")  # للتصحيح
    
    try:
        if table_exists(cours._meta.db_table):
            cour = cours.objects.filter(slug=slug).first()
            print(f"نتيجة البحث في جدول cours: {cour}")  # للتصحيح
            if cour:
                return show_cours(request, slug)
    except Exception as e:
        print(f"خطأ في البحث في جدول cours: {str(e)}")

    # إذا لم يوجد في cours، ابحث في بقية الجداول
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
    path('rock_paper_scissors/', rps_game, name='rock_paper_scissors'),
    path('send_message/', send_message, name='send_message'),
    path('profile/edit/', edit_user, name='edit_user'),
    path('profile/', show_user, name='show_user'),
    
        # مسارات المستخدمين
    path('contacts/', contacts_index, name='contacts'),
    path('users/', members_index, name='users'),
    
    path('users/<int:user_id>/', member_profile_view, name='member_profile_view'),  # لملف شخصي معين
    path('users/<int:user_id>/edit/', edit_member_profile, name='edit_member_profile'),  # لتعديل ملف معين (للمسؤولين)
    path('users/<int:user_id>/delete/', delete_member_profile, name='delete_member_profile'),
    path('users/<int:user_id>/manage-relations/', manage_member_relations, name='manage_member_relations'),
    path('users/<int:user_id>/update-image/', update_profile_image, name='update_profile_image'),
    
    path('contacts/<int:contacts_id>/', contact_view, name='contact_view'),  # لملف شخصي معين
    path('contacts/<int:contacts_id>/edit/', edit_contact, name='edit_contact'),  # لتعديل ملف معين (للمسؤولين)
    path('contacts/create/', contact_create, name='contact_create'),
    
    # لتعديل ملف معين (للمسؤولين)
    path('contacts/<int:contacts_id>/delete/', delete_contact, name='delete_contact'),
    path('contacts/<int:contacts_id>/manage-relations/', manage_contact_relations, name='manage_contact_relations'),
    path('contacts/<int:contacts_id>/update-image/', update_contact_image, name='update_contact_image'),

    #  إنشاء المحتوى
    path('articles/create/', create_content, {'content_type': 'articles'}, name='create_article'),
    path('videos/create/', create_content, {'content_type': 'videos'}, name='create_video'),
    path('books/create/', create_content, {'content_type': 'books'}, name='create_book'),
    path('cours/create/', create_content, {'content_type': 'cours'}, name='create_cours'),
    path('exams/create/', create_content, {'content_type': 'exams'}, name='create_exam'),

    #  تعديل المحتوى المحتوى
    path('articles/edit/<path:slug>/', edit_content, {'content_type': 'articles'}, name='edit_article'),
    path('videos/edit/<path:slug>/', edit_content, {'content_type': 'videos'}, name='edit_video'),
    path('books/edit/<path:slug>/', edit_content, {'content_type': 'books'}, name='edit_book'),
    path('cours/edit/<path:slug>/', edit_content, {'content_type': 'cours'}, name='edit_cours'),
    path('exams/edit/<path:slug>/', edit_content, {'content_type': 'exams'}, name='edit_exam'), 
    path('profile/<int:user_id>/', show_user, name='user_profile'),
    # مسار خاص بـ cours قبل المسار العام
    path('cours/<path:slug>/', show_cours, name='show_cours'),
    
        path("logout/", custom_logout, name="logout"),

    # المحتوى الديناميكي (يجب أن يكون آخر مسار)
    path('<str:slug>/', content_router, name='dynamic_content'),
    path('', welcome, name='welcome'),
]