import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Custom User Model
class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, help_text=_("Unique identifier for the user."))
    email = models.EmailField(unique=True, help_text=_("The user's email address."))
    password = models.CharField(max_length=128, help_text=_("The user's password."))
    first_name = models.CharField(max_length=30, help_text=_("The user's first name."))
    last_name = models.CharField(max_length=150, help_text=_("The user's last name."))
    bio = models.TextField(blank=True, null=True, help_text=_("A short biography about the user."))
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, help_text=_("User's profile photo."))
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text=_("User's phone number."))

    def __str__(self):
        return self.username
