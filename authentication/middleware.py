from django.urls import resolve
from django.conf import settings

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the current path matches any public paths
        path = request.path_info.lstrip('/')
        
        # Skip authentication for public paths
        for public_path in getattr(settings, 'PUBLIC_PATHS', []):
            if public_path.match(path):
                return self.get_response(request)
        
        response = self.get_response(request)
        return response