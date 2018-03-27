from django.urls import path, re_path
from .views import (
    BookShelfView,
    BookLogCreateView,
    BookLogPostCreateView,
    BookLogDetailView,
    BookLogUpdateView,
    BookLogDeleteView
)

app_name = 'shelf'
urlpatterns = [
    path('public/<int:user_id>', BookShelfView.as_view(), name='bookshelf_view'),
    path('private/', BookShelfView.as_view(), name='bookshelf_view_private'),
    path('create/bk<int:book_id>/', BookLogCreateView.as_view(), name='booklog_create'),
    path('blg<int:booklog_id>/', BookLogDetailView.as_view(), name='booklog_detail'),
    path('blg<int:booklog_id>/createpost/', BookLogPostCreateView.as_view(), name='booklog_createpost'),
    path('blg<int:booklog_id>/update/', BookLogUpdateView.as_view(), name='booklog_update'),
    path('blg<int:booklog_id>/delete/', BookLogDeleteView.as_view(), name='booklog_delete'),
]

