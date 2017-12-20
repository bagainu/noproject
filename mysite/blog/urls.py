from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog_index'),
    path('<slug:title_slug>/', views.detail, name='blog_detail'),
]