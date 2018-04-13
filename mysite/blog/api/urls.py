from django.urls import path
from .views import (
    PostListAPIView,
    PostCreateAPIView,
    PostDetailAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView,
)


app_name = 'api'
urlpatterns = [
    path('', PostListAPIView.as_view(), name='blog_index'),
    path('create/', PostCreateAPIView.as_view(), name='blog_create'),
    path('b<int:blog_id>/', PostDetailAPIView.as_view(), name='blog_detail'),
    path('b<int:blog_id>/update/', PostUpdateAPIView.as_view(), name='blog_update'),
    path('b<int:blog_id>/delete/', PostDeleteAPIView.as_view(), name='blog_delete'),
]

