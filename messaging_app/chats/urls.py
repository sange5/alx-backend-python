from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# The router.urls automatically generates the URL patterns for these viewsets
urlpatterns = router.urls
["from django.urls import", "path", "include", "routers.DefaultRouter()"]

from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# The router.urls automatically generates the URL patterns for these viewsets
urlpatterns = router.urls

from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Initialize the DefaultRouter
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Initialize the NestedDefaultRouter for nested message routes
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Combine the default and nested routers
urlpatterns = router.urls + conversation_router.urls
