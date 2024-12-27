"""
URL configuration for messaging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.contrib import admin
from django.urls import path, include

# Include the 'chats' app's URLs with the 'api/' prefix
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('messaging_app.chats.urls')),  # Correctly include the api routes
]

from django.contrib import admin
from django.urls import path, include

# Include the 'chats' app's URLs with the 'api/' prefix
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('messaging_app.chats.urls')),  # Including chat routes under 'api/' prefix
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('messaging_app.chats.urls')),  # Include chats API routes
    path('api-auth/', include('rest_framework.urls')),  # Add this line for authentication
]

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from chats.auth import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('chats.urls')),  # Include your chats app URLs
]

