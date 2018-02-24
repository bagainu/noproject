from django.db import models

from utils.image_utils import image_upload_to
# Create your models here.


class Author(models.Model):
    author_name = models.CharField(max_length=200)
    author_photo = models.ImageField(null=True, blank=True, upload_to=image_upload_to) # upload_to='images'
    author_intro = models.TextField()

    def __str__(self):
        return '{0}'.format(self.author_name)

    def __unicode__(self):
        return '{0}'.format(self.author_name)

    def get_absolute_url(self):
        pass


class Press(models.Model):
    press_name = models.CharField(max_length=200)

    def __str__(self):
        return '{0}'.format(self.press_name)

    def __unicode__(self):
        return '{0}'.format(self.press_name)


class Book(models.Model):
    book_title = models.CharField(max_length=200)
    sub_title = models.CharField(null=True, blank=True, max_length=200)
    book_cover = models.ImageField(null=True, blank=True, upload_to=image_upload_to) # upload_to='images'
    pub_date = models.DateField()
    book_intro = models.TextField()
    book_author = models.ManyToManyField(Author)
    book_press = models.ManyToManyField(Press)

    @property
    def authors(self):
        return ' | '.join([ str(author) for author in self.book_author.all() ])

    @property
    def presses(self):
        return ' | '.join([ str(press) for press in self.book_press.all() ])

    def __str__(self):
        return '{0}'.format(self.book_title)

    def __unicode__(self):
        return '{0}'.format(self.book_title)

    def get_absolute_url(self):
        pass

