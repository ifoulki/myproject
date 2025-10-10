from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.http import Http404
from importlib import import_module
from django.db import connection
from tifinar.models import articles, videos, cours, books, exams, Visitors, AuthUser
from tifinar.views.content.articles import article_detail
from tifinar.views.content.videos import video_detail
from tifinar.views.content.books import book_detail
from tifinar.views.content.content import contents
from tifinar.views.dashboard.dashboard import dashboard_view
from tifinar.views.content.eddit_index import *
from tifinar.views.content.welcome import welcome
from tifinar.views.games.rock_paper_scissors import rps_game
from tifinar.views.audience.msgs import send_message
from tifinar.views.content.cours import show_cours 
from tifinar.views.members.user import show_user 
from tifinar.views.members.members_index import members_index 
from tifinar.views.contacts.contacts_index import contacts_index
from tifinar.views.contacts.create_contact import contact_create
from tifinar.views.members.user import edit_user 
from tifinar.views.members.show_member import *
from tifinar.views.contacts.show_contact import *
from tifinar.views.content_manager.show_create_contents import show_create_content
from tifinar.views.content_manager.article_manager import create_article
from tifinar.views.content_manager.book_manager import create_book
from tifinar.views.content_manager.video_manager import create_video
from tifinar.views.content_manager.create_cours import create_cours
from tifinar.views.content_manager.edit_contents import edit_content
from tifinar.views.content_manager.edit_books import edit_book
from tifinar.views.content_manager.edit_video import edit_video
from tifinar.views.content_manager.edit_cours import edit_cours_view
from tifinar.views.content.exams import exam_view, store_answer
from tifinar.logout import custom_logout
from tifinar.login import custom_login
from tifinar.logup import custom_logup


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

# مسارات التطبيق
urlpatterns = [
    
    path('admin/', admin.site.urls),
    
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
    
    path('users/<int:user_id>/', member_profile_view, name='member_profile_view'),
    path('users/<int:user_id>/edit/', edit_member_profile, name='edit_member_profile'),
    path('users/<int:user_id>/delete/', delete_member_profile, name='delete_member_profile'),
    path('users/<int:user_id>/manage-relations/', manage_member_relations, name='manage_member_relations'),
    path('users/<int:user_id>/update-image/', update_profile_image, name='update_profile_image'),
    
    path('contacts/<int:contacts_id>/', contact_view, name='contact_view'),
    path('contacts/<int:contacts_id>/edit/', edit_contact, name='edit_contact'),
    path('contacts/create/', contact_create, name='contact_create'),
    path('contacts/<int:contacts_id>/delete/', delete_contact, name='delete_contact'),
    path('contacts/<int:contacts_id>/manage-relations/', manage_contact_relations, name='manage_contact_relations'),
    path('contacts/<int:contacts_id>/update-image/', update_contact_image, name='update_contact_image'),

    # إنشاء المحتوى
    path('articles/create/', create_article, name='create_article'),
    path('books/create/', create_book, name='create_book'),
    path('videos/create/', create_video, name='create_video'),
    path('cours/create/', create_cours, name='create_cours'),
    path('exams/create/', show_create_content, {'content_type': 'exams'}, name='create_exam'),

    # حدف المحتوى
    path('articles/delete/<path:slug>/', delete_content, name='delete_article'),
    path('books/delete/<path:slug>/', delete_content, name='delete_books'),
    path('exams/delete/<path:slug>/', delete_content, name='delete_exams'),
    path('cours/delete/<path:slug>/', delete_content, name='delete_cours'),
    path('videos/delete/<path:slug>/', delete_content, name='delete_videos'),

    # تعديل المحتوى
    path('articles/edit/<path:slug>/', edit_content, {'content_type': 'articles'}, name='edit_article'),
    path('videos/edit/<path:slug>/', edit_video,{'content_type': 'videos'}, name='edit_video'),
    path('books/edit/<path:slug>/', edit_book, {'content_type': 'books'}, name='edit_book'),
    path('cours/edit/<slug:slug>/', edit_cours_view, name='edit_cours'),
    path('exams/edit/<path:slug>/', edit_content, {'content_type': 'exams'}, name='edit_exam'), 
    
    path('profile/<int:user_id>/', show_user, name='user_profile'),
    path('exam/store-answer/', store_answer, name='store_answer'),
    path('exams/<path:exam_slug>/', exam_view, name='exam_view'),
    
    path("logout/", custom_logout, name="logout"),
    path("login/", custom_login, name="login"),
    path('logup/', custom_logup, name='logup'),

    # المحتوى الديناميكي (يجب أن يكون آخر مسار)
    path('articles/<str:slug>/', article_detail, name='dynamic_content'),
    path('videos/<str:slug>/', video_detail, name='dynamic_content'),
    path('books/<str:slug>/', book_detail, name='dynamic_content'),
    path('cours/<str:slug>/', show_cours, name='dynamic_content'),
    path('', welcome, name='welcome'),
    
]