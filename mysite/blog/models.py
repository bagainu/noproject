from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.


def image_upload_to(instance, file_name):
    return '''images/{0}_{1}'''.format(instance.id, file_name)


class Post(models.Model):
    blog_title = models.CharField(max_length=200)
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
