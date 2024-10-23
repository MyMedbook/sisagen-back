from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def api_root(request):
    """
    Root endpoint that provides API information
    """
    return Response({
        'status': 'success',
        'message': 'Welcome to MyMedBook API',
        'version': '1.0',
        'endpoints': {
            'auth': {
                'token': '/auth/token/',
                'verify': '/auth/verify/',
            },
            'api': {
                'profile': '/api/profile/',
                'resource': '/api/resource/',
            }
        }
    }, status=status.HTTP_200_OK)

def health_check(request):
    """
    Simple health check endpoint
    """
    return JsonResponse({
        'status': 'healthy',
        'message': 'System is running'
    })