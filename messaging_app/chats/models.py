from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Custom User Model
class User(AbstractUser):
    # Additional fields for the User model
    bio = models.TextField(blank=True, null=True, help_text=_("A short biography about the user."))
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, help_text=_("User's profile photo."))
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text=_("User's phone number."))

    def __str__(self):
        return self.username

# Conversation Model
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations", help_text=_("Users involved in the conversation."))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("The date and time the conversation was created."))

    def __str__(self):
        return f"Conversation {self.id} with {', '.join([user.username for user in self.participants.all()])}"

# Message Model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages", help_text=_("The user who sent the message."))
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages", help_text=_("The conversation this message belongs to."))
    content = models.TextField(help_text=_("The content of the message."))
    timestamp = models.DateTimeField(auto_now_add=True, help_text=_("The date and time the message was sent."))

    def __str__(self):
        return f"Message from {self.sender.username} in Conversation {self.conversation.id}"
