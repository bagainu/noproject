from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

# Helping functions
def image_upload_to(instance, file_name):
    return '''images/{0}_{1}'''.format(instance.id, file_name)


# Models
class Post(models.Model):
    blog_title = models.CharField(max_length=200)
    slug_title = models.SlugField(unique=True) # used for ease of url visiting
    create_date_time = models.DateTimeField(auto_now=False, auto_now_add=True, help_text='data published')
    update_date_time = models.DateTimeField(auto_now=True, auto_now_add=False, help_text='data updated')
    blog_image = models.ImageField(null=True, blank=True, upload_to=image_upload_to) # upload_to='images'
    blog_content = models.TextField()
    blog_author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self):
        return '"{0}" by {1}'.format(self.blog_title, self.blog_author)

    def __unicode__(self):
        return '"{0}" by {1}'.format(self.blog_title, self.blog_author)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={ 'blog_id': self.id, })


class Author(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    reg_time = models.DateTimeField(auto_now=False, auto_now_add=True, help_text='registered')
    user_pwd = models.CharField(max_length=100, default='')

    def __str__(self):
        return '{0} {1} ({2})'.format(self.first_name, self.last_name, self.email)

    def __unicode__(self):
        return '{0} {1} ({2})'.format(self.first_name, self.last_name, self.email)

    def get_absolute_url(self):
        pass


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

