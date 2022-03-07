from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                       PermissionsMixin
from django.conf import settings
from django.utils import timezone

import os
import uuid


def event_image_file_path(instance, filename):
    """Generate file path for new event"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('events/images/', filename)


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not username:
            raise ValueError('Users must have username')

        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        """Creates a new super user and save it"""
        user = self.create_user(username,email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'


class Event(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField(default=timezone.now)
    event_time = models.TimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to=event_image_file_path)

    def __str__(self):
        return self.title
