from django import forms
from django.forms import ModelForm

from pagedown.widgets import PagedownWidget

# Make form of models to use in the views
# Related Links: https://docs.djangoproject.com/en/2.0/topics/forms/modelforms/

from .models import Comment

# class CommentForm(forms.Form):
    # content_type = forms.CharField(widget=forms.HiddenInput)
    # object_id = forms.IntegerField(widget=forms.HiddenInput)
    # #parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # comment_content = forms.CharField(label='', widget=forms.Textarea)

class CommentForm(forms.Form):

    comment_content = forms.CharField(widget=PagedownWidget(show_preview=False), label='')

    class Meta:
        model = Comment
        fields = [
            'comment_content',
        ]
