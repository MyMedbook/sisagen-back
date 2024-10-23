# api/views.py
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from authentication.backends import TokenAuthentication

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Protected endpoint that returns user profile information
    """
    try:
        auth_info = request.auth
        return Response({
            "status": "success",
            "message": "Profile retrieved successfully",
            "data": {
                "auth_token": auth_info.get('token'),
                "token_type": auth_info.get('type', 'Bearer'),
                "permissions": auth_info.get('scope', 'read write groups'),
                "is_authenticated": request.user.is_authenticated
            }
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_resource(request):
    """
    Protected endpoint that creates a new resource
    """
    try:
        data = request.data
        if not data:
            return Response({
                "status": "error",
                "message": "No data provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        auth_info = request.auth
        return Response({
            "status": "success",
            "message": "Resource created successfully",
            "data": {
                "received_data": data,
                "auth_info": {
                    "token": auth_info.get('token'),
                    "token_type": auth_info.get('type', 'Bearer'),
                    "scope": auth_info.get('scope', 'read write groups')
                }
            }
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)