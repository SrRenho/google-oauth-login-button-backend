from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework.response import Response
from rest_framework import status

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request, *args, **kwargs):
        # Call normal login logic
        super().post(request, *args, **kwargs)

        # request.user is now logged in; generate JWT manually
        if request.user.is_authenticated:
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(request.user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'first_name': request.user.first_name,
                    'email': request.user.email,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleIDTokenLogin(APIView):
    def post(self, request):
        token = request.data.get("access_token")
        print("Received token:", token)  # Add this line

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "306304482324-t6okpjml4j4r622160shhoivf9nc1ccc.apps.googleusercontent.com")
            # idinfo has 'email', 'sub', 'name', etc.
            email = idinfo['email']
            user, created = User.objects.get_or_create(email=email, defaults={'username': email.split('@')[0], 'first_name': idinfo.get('given_name', '')})

            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "email": user.email
                }
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            print("Google token verification error:", e)  # Add this line

            return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)
