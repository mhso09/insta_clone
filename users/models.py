from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('C', 'Custom'),
    ]

    name = models.CharField(_('Name of User'), max_length=255, blank=True)
    user_name = models.CharField(blank=True, max_length=255)
    profile_photo = models.ImageField(blank=True)
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    email = models.CharField(blank=True, max_length=255)
    phone_number = models.CharField(blank=True, max_length=255)
    gender = models.CharField(blank=True, max_length=255, choices=GENDER_CHOICES)
    followers = models.ManyToManyField('self')
    following = models.ManyToManyField('self')

    class Meta:
        db_table = 'Users_user'
