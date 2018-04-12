from django.urls import path, re_path
from . import views

app_name = 'myuser'
urlpatterns = [
    path('register/', views.register, name='user_register'),
    path('login/', views.login, name='user_login'),
    path('logout/', views.logout, name='user_logout'),
    path('a<int:user_id>/', views.profile, name='user_profile'),
    path('ajax-follow/a<int:user_id>/', views.ajax_follow, name='ajax_follow'),
    path('ajax-unfollow/a<int:user_id>/', views.ajax_unfollow, name='ajax_unfollow'),
]

