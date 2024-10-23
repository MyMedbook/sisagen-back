from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
@permission_classes([AllowAny])  # Allow public access
def api_root(request):
    """
    Root endpoint that provides API information
    """
    return Response({
        'status': 'success',
        'message': 'Welcome to MyMedBook API',
        'version': '1.0',
        'endpoints': {
            'public': {
                'root': '/',
                'health': '/health/',
                'token': '/auth/token/',
            },
            'protected': {
                'profile': '/api/profile/',
                'resource': '/api/resource/',
                'verify': '/auth/verify/',
            }
        }
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])  # Allow public access
def health_check(request):
    """
    Simple health check endpoint
    """
    return Response({
        'status': 'healthy',
        'message': 'System is running'
    }, status=status.HTTP_200_OK)