from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.template.defaultfilters import linebreaks
from django.urls import reverse
from django.utils.html import format_html

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from shelf.models import BookLog
from comments.models import Comment
# Create your models here.

class ShareTag(TaggedItemBase):
    content_object = models.ForeignKey('BookShareList', on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name

    def __unicode__(self):
        return self.tag.name


class BookShareList(models.Model):
    share_user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    share_title = models.CharField(max_length=200)
    share_intro = models.TextField(max_length=1024, blank=True)
    share_books = models.ManyToManyField(BookLog, blank=True) # at lease has one book
    share_create_date_time = models.DateTimeField(auto_now=False, auto_now_add=True, help_text='share published')
    share_update_date_time = models.DateTimeField(auto_now=True, auto_now_add=False, help_text='share updated')
    share_comment = GenericRelation(Comment, related_query_name='share_comment')
    share_tag = TaggableManager(through=ShareTag, blank=True)

    def __str__(self):
        return self.share_title

    def __unicode__(self):
        return self.share_title

    def get_absolute_url(self):
        return reverse('sharelist:share_detail', kwargs={ 'share_id': self.id, })

    def get_intro_content_html(self):
        return format_html(linebreaks(self.share_intro))
