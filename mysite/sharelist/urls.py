from django.urls import path, re_path
from .views import (
    ShareListCreateView,
    ShareListDeleteView,
    ShareListDetailView,
    ShareListIndexView,
    ShareListIndexOwnView,
    ShareListUpdateView,
)


app_name = 'sharelist'
urlpatterns = [
    path('', ShareListIndexView.as_view(), name='share_index'),
    path('own/<int:user_id>/', ShareListIndexOwnView.as_view(), name='share_index_own'),
    path('create/', ShareListCreateView.as_view(), name='share_create'),
    path('bsl<int:share_id>/', ShareListDetailView.as_view(), name='share_detail'),
    path('bsl<int:share_id>/update/', ShareListUpdateView.as_view(), name='share_update'),
    path('bsl<int:share_id>/delete/', ShareListDeleteView.as_view(), name='share_delete'),
]
