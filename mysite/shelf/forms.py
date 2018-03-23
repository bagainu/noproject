from django import forms
from django.forms import ModelForm

from ckeditor.widgets import CKEditorWidget

from .models import BookLog


class BookLogForm(ModelForm):

    booklog_intro = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = BookLog
        fields = [
            'booklog_intro',
            # 'booklog_rates',
            # 'booklog_comment',
            # 'booklog_post',
        ]
