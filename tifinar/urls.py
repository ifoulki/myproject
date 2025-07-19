from django.urls import path
from . import views

app_name = "tifinar"

urlpatterns = [
    path('contents/', views.contents, name='contents'),                # لقائمة المقالات
    path('<str:slug>/', views.showContent, name='showContent'),  # لعرض مقال حسب slug
    path('store-reaction/', views.store_reaction, name='store_reaction'),
]
