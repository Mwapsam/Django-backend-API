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
    def _create_user(self, firstname, lastname, email, phoneNumber, password=None, **extra_fields):
        if not firstname:
            raise ValueError('The given firstname must be set')

        if not lastname:
            raise ValueError('The given lastname must be set')

        if not email:
            raise ValueError('The given email must be set')

        if not phoneNumber:
            raise ValueError('The given phone number must be set')

        email = self.normalize_email(email)
        user = self.model(firstname=firstname, lastname=lastname, email=email, phoneNumber=phoneNumber, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, firstname, lastname, email, phoneNumber, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(firstname, lastname, email, phoneNumber, password, **extra_fields)

    def create_superuser(self, firstname, lastname, email, phoneNumber, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(firstname, lastname, email, phoneNumber, password, **extra_fields)

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

    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('fistname', 'lastname')

    objects = UserManager()

    def __str__(self):
        return self.firstname

    def get_full_name(self):
        return self.firstname

    def get_short_name(self):
        return self.firstname

        