from django.urls import path
from . import views

app_name = "tifinar"

urlpatterns = [
    path('contents/', views.contents, name='contents'),                # لقائمة المقالات
    path('contents/<str:slug>/', views.showContent, name='showContent'),  # لعرض مقال حسب slug
]
