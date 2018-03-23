from django.urls import path, re_path
from .views import (
    BookShelfView,
    BookLogCreateView,
    BookLogDetailView,
    BookLogUpdateView,
    BookLogDeleteView
)

app_name = 'shelf'
urlpatterns = [
    path('', BookShelfView.as_view(is_public=True), name='bookshelf_view'),
    path('private/', BookShelfView.as_view(is_public=False), name='bookshelf_view_private'),
    path('create/', BookLogCreateView.as_view(), name='booklog_create'),
    path('blg<int:booklog_id>/', BookLogDetailView.as_view(), name='booklog_detail'),
    path('blg<int:booklog_id>/update/', BookLogUpdateView.as_view(), name='booklog_update'),
    path('blg<int:booklog_id>/delete/', BookLogDeleteView.as_view(), name='booklog_delete'),
]

