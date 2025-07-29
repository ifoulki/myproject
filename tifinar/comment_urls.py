from django.urls import path
from . import views

app_name = 'tifinar_comments'

urlpatterns = [
    path('post/', views.store_comment, name='store_comment'),
]