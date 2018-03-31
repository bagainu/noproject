from django import forms
from django.forms import ModelForm

from ckeditor.widgets import CKEditorWidget
from taggit.forms import TagField, TagWidget

from .models import BookShareList


class BookShareListForm(ModelForm):

    share_intro = forms.CharField(widget=CKEditorWidget())
    share_tag = TagField(widget=TagWidget(), required=False, help_text='A comma-separated list of tags.')

    class Meta:
        model = BookShareList
        fields = [
            'share_title',
            'share_intro',
            'share_tag',
        ]
