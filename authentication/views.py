# authentication/views.py
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings

class ObtainTokenView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Obtain token from external OAuth2 provider
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': settings.OAUTH2_PROVIDER['AUTHORIZATION_HEADER']
        }
        
        data = {
            'grant_type': 'password',
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'client_id': settings.OAUTH2_PROVIDER['CLIENT_ID'],
            'client_secret': settings.OAUTH2_PROVIDER['CLIENT_SECRET']
        }
        
        try:
            response = requests.post(
                settings.OAUTH2_PROVIDER['TOKEN_URL'],
                headers=headers,
                data=data
            )
            
            # Forward the response from the OAuth2 provider
            return Response(
                response.json(),
                status=response.status_code
            )
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_token(request):
    """
    Verify if a token is valid
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith('Bearer '):
        return Response(
            {'error': 'Invalid authorization header'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token = auth_header.split(' ')[1]
    return Response({
        'valid': True,
        'token': token
    })