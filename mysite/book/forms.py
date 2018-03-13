from django import forms
from django.forms import ModelForm

from pagedown.widgets import PagedownWidget
from ckeditor.widgets import CKEditorWidget
from taggit.forms import TagField, TagWidget

from utils.image_utils import PreviewImageWidget
from utils.time_utils import YEAR_CHOICES, CustomSelectDateWidget
from .models import Book, Author, Press


class BookForm(ModelForm):

    book_intro = forms.CharField(widget=CKEditorWidget())
    book_tag = TagField(widget=TagWidget(), required=False, help_text='A comma-separated list of tags.')
    # pub_date = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES))
    pub_date = forms.DateField(widget=CustomSelectDateWidget(years=YEAR_CHOICES))
    book_cover = forms.ImageField(widget=PreviewImageWidget())

    class Meta:
        model = Book
        fields = [
            'book_title',
            'sub_title',
            'book_cover',
            'pub_date',
            'book_intro',
            'book_author',
            'book_press',
            'book_tag',
        ]


class AuthorForm(ModelForm):

    author_intro = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Author
        fields = [
            'author_name',
            'author_photo',
            'author_intro',
        ]


class PressForm(ModelForm):

    class Meta:
        model = Press
        fields = [
            'press_name',
        ]

