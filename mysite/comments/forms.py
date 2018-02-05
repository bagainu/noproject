from django import forms
from django.forms import ModelForm

from pagedown.widgets import PagedownWidget
from ckeditor.widgets import CKEditorWidget

# Make form of models to use in the views
# Related Links: https://docs.djangoproject.com/en/2.0/topics/forms/modelforms/

from .models import Comment

# class CommentForm(forms.Form):
#     content_type = forms.CharField(widget=forms.HiddenInput)
#     object_id = forms.IntegerField(widget=forms.HiddenInput)
#     comment_content = forms.CharField(label='', widget=PagedownWidget(show_preview=False))

class CommentForm(ModelForm):

    # comment_content = forms.CharField(widget=PagedownWidget(show_preview=False), label='')
    comment_content = forms.CharField(widget=CKEditorWidget(), label='')

    class Meta:
        model = Comment
        fields = [
            'comment_content',
        ]
