from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_NULL
from django.core.validators import RegexValidator
from .managers import UserManager

phone_regex = RegexValidator(
    regex=r'^\d{10}$', message="Phone number should be of format +971*********")


class User(AbstractUser):
    """
    Custom User model which extends from the BaseUser Model of Django
    """
    gender_choice = [("M", "Male"), ("F", "Female"), ("O", "Others")]
    user_type_choice = [("app", "App"), ("dashboard", "Dashboard")]
    city_choices = [("AUH", "Abu Dhabi"), ("DXB", "Dubai"), ("SHJ", "Sharjah"), ("AJM",
                                                                                 "Ajman"), ("UAQ", "Umm Al Quwain"), ("RAK", "Ras Al Khaimah"), ("FUJ", "Fujairah")]

    username = None
    email = models.EmailField(
        verbose_name='Email Address', max_length=255, unique=True, db_index=True)
    phone = models.CharField(
        validators=[phone_regex], verbose_name='Mobile Number', max_length=10, unique=True, db_index=True)
    city = models.CharField(choices=city_choices,
                            verbose_name="City", max_length=255, default="DXB")
    gender = models.CharField(choices=gender_choice,
                              max_length=10, blank=True, null=True)
    user_type = models.CharField(choices=user_type_choice,
                                 verbose_name="User type for permissions", max_length=255, default="app")
    profile_img = models.ImageField(
        upload_to="profile", verbose_name="Profile image", blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    objects = UserManager()

    class Meta:
        """
        Meta data for UserDB model
        """
        permissions = [
            ('app_user', 'App User Permissions'),  # usage: 'users.app_user'
            # usage: 'users.dashboard_user'
            ('dashboard_user', 'Dashboard User Permissions'),
        ]
        db_table = 'ra_users'

    def __str__(self) -> str:
        return self.email
