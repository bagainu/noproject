from django.db import models

# Create your models here.

class Contents(models.Model):
    blog_title = models.CharField(max_length=200)
    date_time = models.DateTimeField('data published')
    blog_content = models.TextField()
    blog_author = models.ForeignKey('Author', on_delete=models.CASCADE)

    def __str__(self):
        return '"{0}" by {1}'.format(self.blog_title, self.blog_author)


class Author(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    reg_time = models.DateTimeField('registered')

    def __str__(self):
        return '{0} {1} ({2})'.format(self.first_name, self.last_name, self.email)

