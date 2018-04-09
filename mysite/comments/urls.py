from django.urls import path, re_path
from . import views


app_name = 'comments'
urlpatterns = [
    path('c<int:comment_id>/', views.detail, name='comment_detail'),
    path('c<int:comment_id>/delete/', views.delete, name='comment_delete'),
    path('ajax-vote-up/c<int:comment_id>/', views.ajax_vote_up, name='ajax_vote_up'),
]

