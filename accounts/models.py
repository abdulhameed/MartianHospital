from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


#  Custom User model.
class User(AbstractUser):
    GENDER = 'G'
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = [
        (GENDER, 'Gender'),
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    is_staff = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    username = None
    email = models.EmailField('email address', unique=True)
    phone = models.CharField(max_length=16, blank=True, null=True, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default=GENDER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


#     create foreign keys to the User model importing the settings from django.conf import settings
#     and referring to the settings.AUTH_USER_MODEL instead of referring directly to the custom User model.


class Patient(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)


class DocProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True,
                                 related_name='staff_profile')
    state = models.CharField(max_length=30, default='Lagos')

    def __str__(self):
        return f'{self.user.email}'


