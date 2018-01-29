from django.urls import path, re_path
from . import views


app_name = 'comments'
urlpatterns = [
    path('c<int:comment_id>/', views.detail, name='comment_detail'),
    path('delete/c<int:comment_id>/', views.delete, name='comment_delete'),
]

