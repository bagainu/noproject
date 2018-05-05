from django.urls import path, re_path
from .views import IndexView


app_name = 'common'
urlpatterns = [
    path('', IndexView.as_view(), name='common_index'),
]