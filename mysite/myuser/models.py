from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager,
    # Base class of built-in permissions
    # link: https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#custom-users-and-permissions
    # PermissionsMixin, 
)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import linebreaks
from django.urls import reverse
from django.utils.html import format_html

from shelf.models import BookShelf

from utils.image_utils import image_upload_to
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **kwargs):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **kwargs):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            kwargs=kwargs
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class CustomUser(AbstractBaseUser):
    MALE = 0
    FEMALE = 1
    OTHER = 2
    GENDER_CHOICES =(
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=200)
    register_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=OTHER)
    avatar = models.ImageField(null=True, blank=True, upload_to=image_upload_to)
    intro = models.TextField(blank=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_following')
    followed = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_followed')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username', 
        ]

    objects = CustomUserManager()
    
    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_intro_html(self):
        return format_html(linebreaks(self.intro))

    @property
    def gender_name(self):
        return self.GENDER_CHOICES[self.gender][1]

    def get_absolute_url(self):
        return reverse('myuser:user_profile', kwargs={ 'user_id': self.id })


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save_callback(sender, instance, created, *args, **kwargs):
    if created:
        try:
            BookShelf.objects.get_or_create(shelf_owner=instance)
        except:
            pass
