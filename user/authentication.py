from datetime import datetime, timedelta

import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

from user.models import User
from user.serializer import UserSerializer

class JWTAuthentication(authentication.BaseAuthentication):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)  # clean the token

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Token invalide !!!')
        except:
            raise ParseError('Token expiré, veuillez le renouveler.')

        # Get the user from the database
        user_id = payload.get('user_id')
        if user_id is None:
            raise AuthenticationFailed('Id de l\'utilisateur non trouvé.')

        user = User.objects.filter(id=user_id).first()
        if user is None:
            raise AuthenticationFailed('Utilisateur non identifié !!!')
        
        now = datetime.now()
        exp = datetime.fromtimestamp(int(payload.get('exp')))
        
        if now > exp:
            raise AuthenticationFailed('Token expiré !!!')

        # Return the user and token payload
        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user):
        # Create the JWT payload
        payload = {
            'user_id': str(user.id),
            'email': user.email,
            'iat': datetime.now().timestamp(),
            'exp': int((datetime.now() + timedelta(days=settings.JWT_CONF['TOKEN_LIFETIME_HOURS'])).timestamp()),
            # set the expiration time for 1 day from now
        }

        # Encode the JWT with your secret key
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token