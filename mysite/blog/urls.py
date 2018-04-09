from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='blog_index'),
    path('own/<int:user_id>', views.index_own, name='blog_index_own'),
    path('create/', views.create, name='blog_create'),
    path('b<int:blog_id>/', views.detail, name='blog_detail'),
    path('b<int:blog_id>/update/', views.update, name='blog_update'),
    path('b<int:blog_id>/delete/', views.delete, name='blog_delete'),
    path('ajax-vote-up/b<int:blog_id>/', views.ajax_vote_up, name='ajax_vote_up'),
    # re_path('login/(?P<author_id>[0-9]*)', views.login, name='blog_login'),
    # path('response_page/', views.response_page, name='blog_response_page')
]

