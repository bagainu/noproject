from django.urls import path, re_path

from .views import (
    BookIndexView,
    BookCreateView,
    BookDetailView,
    BookUpdateView,
    BookDeleteView,

    AuthorIndexView,
    AuthorCreateView,
    AuthorDetailView,
    AuthorUpdateView,
    AuthorDeleteView,

    PressIndexView,
    PressCreateView,
    PressDetailView,
    PressUpdateView,
    PressDeleteView
)


app_name = 'book'
urlpatterns = [
    # Book
    path('', BookIndexView.as_view(), name='book_index'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('bk<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('bk<int:book_id>/update/', BookUpdateView.as_view(), name='book_update'),
    path('bk<int:book_id>/delete/', BookDeleteView.as_view(), name='book_delete'),

    # Author
    path('author/', AuthorIndexView.as_view(), name='author_index'),
    path('author/create/', AuthorCreateView.as_view(), name='author_create'),
    path('author/ar<int:author_id>/', AuthorDetailView.as_view(), name='author_detail'),
    path('author/ar<int:author_id>/update/', AuthorUpdateView.as_view(), name='author_update'),
    path('author/ar<int:author_id>/delete/', AuthorDeleteView.as_view(), name='author_delete'),

    # Press
    path('press/', PressIndexView.as_view(), name='press_index'),
    path('press/create/', PressCreateView.as_view(), name='press_create'),
    path('press/ps<int:press_id>/', PressDetailView.as_view(), name='press_detail'),
    path('press/ps<int:press_id>/update/', PressUpdateView.as_view(), name='press_update'),
    path('press/ps<int:press_id>/delete/', PressDeleteView.as_view(), name='press_delete'),
]

