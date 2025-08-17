from django.urls import path
from tifinar.views.content.articles import article_detail  # الاستيراد من المسار الصحيح

urlpatterns = [
    # ... مسارات أخرى ...
    path('<str:slug>/', article_detail, name='article_detail'),
]
