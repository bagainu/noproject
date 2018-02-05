from django import forms
from django.forms import ModelForm

from pagedown.widgets import PagedownWidget
from ckeditor.widgets import CKEditorWidget

# Make form of models to use in the views
# Related Links: https://docs.djangoproject.com/en/2.0/topics/forms/modelforms/
from .models import Post


class PostForm(ModelForm):

    # blog_content = forms.CharField(widget=PagedownWidget(show_preview=False))
    blog_content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = [
            'blog_title',
            'blog_content',
            'blog_image',
        ]