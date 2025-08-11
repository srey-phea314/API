# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AccessToken

class QueryParamAccessTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        if not token:
            return None  # No token provided, no authentication

        try:
            access_token = AccessToken.objects.get(token=token, is_active=True)
        except AccessToken.DoesNotExist:
            raise AuthenticationFailed('Invalid or inactive token')

        return (access_token.user, access_token)
