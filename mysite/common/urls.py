from django.urls import path, re_path
from .views import IndexView, ajax_tab_list


app_name = 'common'
urlpatterns = [
    path('', IndexView.as_view(), name='common_index'),
    path('ajax-tab-list/b<int:tab_id>', ajax_tab_list, name='ajax-tab-list'),
]