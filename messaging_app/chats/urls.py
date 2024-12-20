from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# The router.urls automatically generates the URL patterns for these viewsets
urlpatterns = router.urls

["from django.urls import", "path", "include", "routers.DefaultRouter()"]
