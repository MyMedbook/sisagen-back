# authentication/middleware.py
import re
# authentication/middleware.py
from django.conf import settings

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get path without leading slash
        path = request.path_info.lstrip('/')
        
        # Skip authentication for public paths
        if settings.PUBLIC_PATHS.match(path):
            return self.get_response(request)
        
        response = self.get_response(request)
        return response