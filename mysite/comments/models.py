from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.template.defaultfilters import linebreaks
from django.utils.html import format_html

from markdown_deux import markdown
# from blog.models import Post
# Create your models here.


class Comment(models.Model):
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    # comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment_content = models.TextField()
    comment_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}'s comment at {1}".format(self.comment_user, self.comment_date_time)

    def __unicode__(self):
        return "{0}'s comment at {1}".format(self.comment_user, self.comment_date_time)

    def get_comment_content_markdown(self):
        return format_html(linebreaks(markdown(self.comment_content)))
