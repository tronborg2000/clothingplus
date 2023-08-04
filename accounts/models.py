from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from accounts.utils import get_username_unique_slug


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email is required")
        email = self.normalize_email(email)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """creates new superuser with details """

        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=False)
    username = models.CharField(max_length=100, unique=True, db_index=True)
    username_slug = models.SlugField(max_length=200, db_index=True, blank=True, null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.username_slug and self.pk:
            slug_str = f'{self.username}'
            self.username_slug = get_username_unique_slug(self, slug_str, User.objects)

        super().save(*args, **kwargs)

    @property
    def full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()