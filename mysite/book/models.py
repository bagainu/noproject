from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import linebreaks
from django.urls import reverse
from django.utils.html import format_html

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from star_ratings.models import Rating, UserRating

from utils.image_utils import image_upload_to

from comments.models import Comment
# Create your models here.


class BookTag(TaggedItemBase):
    content_object = models.ForeignKey('Book', on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name

    def __unicode__(self):
        return self.tag.name


class Book(models.Model):
    book_title = models.CharField(max_length=200)
    sub_title = models.CharField(null=True, blank=True, max_length=200)
    book_cover = models.ImageField(null=True, blank=True, upload_to=image_upload_to) # upload_to='images'
    pub_date = models.DateField()
    book_intro = models.TextField()
    book_author = models.ManyToManyField('Author')
    book_press = models.ManyToManyField('Press')
    book_tag = TaggableManager(through=BookTag, blank=True)
    # use common/star_rating.html for average rates and common/star_rating_user.html for user rates
    book_rates = GenericRelation(Rating, related_query_name='book_rates')

    @property
    def authors(self):
        return ' | '.join([ str(author) for author in self.book_author.all() ])

    @property
    def presses(self):
        return ' | '.join([ str(press) for press in self.book_press.all() ])

    @property
    def tags(self):
        return ' | '.join([ tag.name for tag in self.blog_tag.all() ])

    def __str__(self):
        return '{0}'.format(self.book_title)

    def __unicode__(self):
        return '{0}'.format(self.book_title)

    def get_absolute_url(self):
        return reverse('book:book_detail', kwargs={ 'book_id': self.id, })

    def get_book_intro_html(self):
        return format_html(linebreaks(self.book_intro))


class Author(models.Model):
    author_name = models.CharField(max_length=200)
    author_photo = models.ImageField(null=True, blank=True, upload_to=image_upload_to) # upload_to='images'
    author_intro = models.TextField()
    author_birth_date = models.DateField(null=True, blank=True)
    author_death_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{0}'.format(self.author_name)

    def __unicode__(self):
        return '{0}'.format(self.author_name)

    def get_absolute_url(self):
        return reverse('book:author_detail', kwargs={ 'author_id': self.id, })

    def get_author_intro_html(self):
        return format_html(self.author_intro)


class Press(models.Model):
    press_name = models.CharField(max_length=200)

    def __str__(self):
        return '{0}'.format(self.press_name)

    def __unicode__(self):
        return '{0}'.format(self.press_name)

    def get_absolute_url(self):
        return reverse('book:press_detail', kwargs={ 'press_id': self.id, })

