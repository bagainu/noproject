from django.forms import ModelForm

# Make form of models to use in the views
# Related Links: https://docs.djangoproject.com/en/2.0/topics/forms/modelforms/
from .models import Post, Author


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'blog_title',
            'blog_content',
            'blog_image',
            'blog_author',
        ]