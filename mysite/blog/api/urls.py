from django.urls import path
from .views import (
    PostListAPIView,
)


app_name = 'api'
urlpatterns = [
    path('', PostListAPIView.as_view(), name='blog_index'),
]

