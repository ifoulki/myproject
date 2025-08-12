from django.urls import path
from . import views
from .views import serve_pdf, send_message
from . import api_views
from .api_views import content_detail 

urlpatterns = [

    # المسارات العامة
    path('store-reaction/', views.store_reaction, name='store_reaction'),
    path('send_message/', send_message, name='send_message'),
    path('game/', views.rps_game, name='game'),
    path('files/<str:filename>', serve_pdf, name='serve_pdf'),
    path('store_comment/', views.store_comment, name='store_comment'),
    path('post/', views.store_comment, name='post_comment'),
    path('comments/', views.comment_view, name='comment_view'),

    # مسارات عرض المحتوى حسب النوع
    path('مقالات/', views.contents, {'content_type': 'articles'}, name='articles'),
    path('اختبارات/', views.contents, {'content_type': 'exams'}, name='exams'),
    path('فيديوهات/', views.contents, {'content_type': 'videos'}, name='videos'),
    path('قواميس_بصرية/', views.contents, {'content_type': 'cours'}, name='cours'),
    path('مكتبة_تيفيناغ/', views.contents, {'content_type': 'books'}, name='books'),

    # المسارات الإدارية (تم تغيير البادئة من admin/ إلى adm/)
    path('profile/', views.show_user, name='show_profile'),
    path('adm/dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_user, name='edit_user'),
    path('profile/<int:user_id>/', views.show_user, name='show_user'),    

    path('videos_edit/', views.index_edit, name='index_video'),
    path('books_edit/', views.index_edit, name='index_book'),
    path('articles_edit/', views.index_edit, name='index_article'),
    path('cours_edit/', views.index_edit, name='index_cours'),
    path('exams_edit/', views.index_edit, name='index_exam'),
    path('', views.welcome, name='welcome'),

    # مسارات إنشاء المحتوى
    path('articles/create/', views.create_content, {'content_type': 'articles'}, name='create_article'),
    path('books/create/', views.create_content, {'content_type': 'books'}, name='create_book'),
    path('cours/create/', views.create_content, {'content_type': 'cours'}, name='create_cours'),
    path('videos/create/', views.create_content, {'content_type': 'videos'}, name='create_video'),
    path('exams/create/', views.create_content, {'content_type': 'exams'}, name='create_exam'),
    
    # مسارات تعديل المحتوى
    path('videos/edit/<str:slug>/', views.edit_content, {'content_type': 'videos'}, name='edit_video'),
    path('exams/edit/<str:slug>/', views.edit_content, {'content_type': 'exams'}, name='edit_exam'),
    path('cours/edit/<str:slug>/', views.edit_content, {'content_type': 'cours'}, name='edit_cours'),
    path('articles/edit/<str:slug>/', views.edit_content, {'content_type': 'articles'}, name='edit_article'),
    path('books/edit/<str:slug>/', views.edit_content, {'content_type': 'books'}, name='edit_book'),
    path('api/content/<slug:slug>/', content_detail, name='content-detail'),

    # مسار عرض المحتوى الفردي (يجب أن يكون في النهاية)
    path('<str:slug>/', views.showContent, name='show_content'),
]