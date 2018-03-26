from django import forms
from django.forms import ModelForm

from ckeditor.widgets import CKEditorWidget

from .models import BookLog


class BookLogForm(ModelForm):

    class Meta:
        model = BookLog
        fields = [
            # 'booklog_rates',
            # 'booklog_comment',
            # 'booklog_post',
        ]
