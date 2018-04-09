from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import linebreaks
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import format_html
from django.urls import reverse

from markdown_deux import markdown
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from vote.models import VoteModel

from utils.image_utils import image_upload_to
from comments.models import Comment
# Create your models here.


class PostTag(TaggedItemBase):
    content_object = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name

    def __unicode__(self):
        return self.tag.name

# Models
class Post(VoteModel, models.Model):
    blog_title = models.CharField(max_length=200)
    slug_title = models.SlugField(unique=True) # used for ease of url visiting
    create_date_time = models.DateTimeField(auto_now=False, auto_now_add=True, help_text='data published')
    update_date_time = models.DateTimeField(auto_now=True, auto_now_add=False, help_text='data updated')
    # blog_image = models.ImageField(null=True, blank=True, upload_to=image_upload_to) # upload_to='images'
    blog_content = models.TextField()
    blog_comment = GenericRelation(Comment, related_query_name='blog_comment')
    blog_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog_tag = TaggableManager(through=PostTag, blank=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()

    def __str__(self):
        return '"{0}" by {1}'.format(self.blog_title, self.blog_author)

    def __unicode__(self):
        return '"{0}" by {1}'.format(self.blog_title, self.blog_author)

    @property
    def tags(self):
        return ' | '.join([ tag.name for tag in self.blog_tag.all() ])

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={ 'blog_id': self.id })

    def get_blog_content_markdown(self):
        return format_html(linebreaks(markdown(self.blog_content)))

    def get_blog_content_html(self):
        return format_html(self.blog_content)


# Signal handlers
# Related links: https://docs.djangoproject.com/en/2.0/ref/signals/

# Connect to signal
# or use: pre_save.connect(post_pre_save_handler, sender=Post)
# Related links: https://stackoverflow.com/questions/6461989/populating-django-field-with-pre-save
@receiver(pre_save, sender=Post)
def post_pre_save_callback(sender, instance, *args, **kwargs):
    slug = slugify(instance.blog_title)
    if Post.objects.filter(slug_title=slug).exists():
        slug = '''{0}-{1}'''.format(slug, str(timezone.now().timestamp()).split('.')[1])
    instance.slug_title = slug


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save_callback(sender, instance, *args, **kwargs):
    pass
