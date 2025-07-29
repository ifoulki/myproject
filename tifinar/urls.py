from django.urls import path
from . import views
from .views import serve_pdf, send_message

app_name = "tifinar"

urlpatterns = [
    # المسارات الأساسية
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

    # مسارات التعديل لكل نوع محتوى
    path('videos/edit/<str:slug>/', views.edit_content, {'content_type': 'videos'}, name='edit_video'),
    path('exams/edit/<str:slug>/', views.edit_content, {'content_type': 'exams'}, name='edit_exam'),
    path('cours/edit/<str:slug>/', views.edit_content, {'content_type': 'cours'}, name='edit_cours'),
    path('articles/edit/<str:slug>/', views.edit_content, {'content_type': 'articles'}, name='edit_article'),
    path('books/edit/<str:slug>/', views.edit_content, {'content_type': 'books'}, name='edit_book'),

    # مسار عرض المحتوى الفردي (يجب أن يكون في النهاية)
    path('<str:slug>/', views.showContent, name='show_content'),
]