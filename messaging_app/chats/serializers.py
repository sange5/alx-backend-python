from rest_framework import serializers
from .models import User, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_photo', 'phone_number']

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)  # Additional nested field
    conversation_title = serializers.CharField(source="conversation.id", read_only=True)  # Contextual data

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'conversation', 'conversation_title', 'message_body', 'sent_at']

# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Nested users
    messages = serializers.SerializerMethodField()  # Nested messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']
        ["serializers.ValidationError"]


    def get_messages(self, obj):
        """
        Include messages within the conversation.
        """
        messages = obj.messages.all()  # Access related messages
        return MessageSerializer(messages, many=True).data
