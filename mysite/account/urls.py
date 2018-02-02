from django.urls import path, re_path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.register, name='user_register'),
    path('login/', views.login, name='user_login'),
    path('logout/', views.logout, name='user_logout'),
]

