from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, creating, retrieving, updating, and deleting conversations.
    """
    queryset = Conversation.objects.prefetch_related('participants', 'messages').all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']  # Allow search by participant username

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        Requires a list of participant user IDs.
        """
        participants = request.data.get('participants')
        if not participants:
            return Response(
                {"error": "Participants are required to create a conversation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, creating, retrieving, updating, and deleting messages.
    """
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']  # Allow ordering messages by sent time

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Requires sender ID, conversation ID, and message body.
        """
        sender = request.data.get('sender')
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not sender or not conversation_id or not message_body:
            return Response(
                {"error": "Sender, conversation, and message body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        message = Message.objects.create(
            sender_id=sender,
            conversation=conversation,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
