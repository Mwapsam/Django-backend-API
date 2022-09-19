from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_manager = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    firstname = models.CharField(db_index=True, max_length=255, unique=True)
    lastname = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
        )

    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length = 16, unique = True)

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ('firstname',)

    objects = UserManager()

    def __str__(self):
        return self.firstname

    def get_full_name(self):
        return self.firstname

    def get_short_name(self):
        return self.firstname

        