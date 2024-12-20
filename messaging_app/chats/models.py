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

# Conversation Model
class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, help_text=_("Unique identifier for the conversation."))
    participants = models.ManyToManyField(User, related_name="conversations", help_text=_("Users involved in the conversation."))
    created_at = models.DateTimeField(auto_now_add=True, help_text=_("The date and time the conversation was created."))

    def __str__(self):
        participant_names = ", ".join(participant.username for participant in self.participants.all())
        return f"Conversation ({self.conversation_id}): {participant_names}"

# Message Model
class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, help_text=_("Unique identifier for the message."))
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages", help_text=_("The user who sent the message."))
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages", help_text=_("The conversation this message belongs to."))
    message_body = models.TextField(help_text=_("The content of the message."))
    sent_at = models.DateTimeField(auto_now_add=True, help_text=_("The date and time the message was sent."))

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.username}"
