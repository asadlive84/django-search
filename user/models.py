from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False, blank=True, null=True)
    is_staff = models.BooleanField(default=True, blank=True, null=True)
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class SearchHistory(models.Model):
    user = models.ManyToManyField(CustomUser)
    search_keyword = models.TextField()
    keyword_count_by_user = models.IntegerField(default=1)
    keyword_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
