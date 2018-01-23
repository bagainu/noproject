from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='blog_index'),
    path('create/', views.create, name='blog_create'),
    path('b<int:blog_id>/', views.detail, name='blog_detail'),
    path('update/b<int:blog_id>/', views.update, name='blog_update'),
    path('delete/b<int:blog_id>/', views.delete, name='blog_delete'),
    # re_path('login/(?P<author_id>[0-9]*)', views.login, name='blog_login'),
    # path('response_page/', views.response_page, name='blog_response_page')
]

