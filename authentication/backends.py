# authentication/backends.py
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
import requests

class TokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Get the authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        try:
            # Split the header into type and token
            auth_type, token = auth_header.split(' ')
            if auth_type.lower() != 'bearer':
                return None
            
            # get user profile from main mymedbook server
            profile_url = "https://mymedbook.it/api/v1/profile/"
            headers = {"Authorization": auth_header}
            response = requests.get(
                profile_url,
                headers=headers
            )

            content = response.json()
            if (status := response.status_code) != 200:
                raise Exception(f"Error during MyMedBook authentication: {content["detail"]} ({status})")

            # Create a user-like object with necessary attributes
            auth_user = type('AuthUser', (), {
                **content,
                'is_authenticated': True,
                'is_active': content["active"],
                'token': token
            })()            

            # Return both the user-like object and the auth info
            return (auth_user, {
                'token': token,
                'type': 'bearer',
                'scope': 'read write groups'
            })

        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid token header')
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))

    def authenticate_header(self, request):
        return 'Bearer'