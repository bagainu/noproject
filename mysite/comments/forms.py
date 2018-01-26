from django import forms
from django.forms import ModelForm

from pagedown.widgets import PagedownWidget

# Make form of models to use in the views
# Related Links: https://docs.djangoproject.com/en/2.0/topics/forms/modelforms/

from .models import Comment


class CommentForm(ModelForm):

    comment_content = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = Comment
        fields = [
            'comment_content',
        ]
