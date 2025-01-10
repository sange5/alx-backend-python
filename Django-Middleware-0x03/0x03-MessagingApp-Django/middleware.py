# Django-Middleware-0x03/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import time

class OffensiveLanguageMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = {}

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            current_time = time.time()

            if ip not in self.message_logs:
                self.message_logs[ip] = []

            # Clean up old messages
            self.message_logs[ip] = [timestamp for timestamp in self.message_logs[ip] if current_time - timestamp < 60]

            # Check if the user has exceeded the limit
            if len(self.message_logs[ip]) >= 5:
                return JsonResponse({'error': 'Message limit exceeded. Please wait a minute before sending more messages.'}, status=429)

            # Log the current message
            self.message_logs[ip].append(current_time)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
# Django-Middleware-0x03/role_permission_middleware.py

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class RolePermissionMiddleware(MiddlewareMixin):
    def __call__(self, request):
        # Assuming the user's role is stored in the request object, e.g., request.user.role
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        user_role = getattr(user, 'role', None)
        
        if user_role not in ['admin', 'moderator']:
            return JsonResponse({'error': 'Forbidden: You do not have permission to perform this action.'}, status=403)

        response = self.get_response(request)
        return response