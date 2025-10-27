from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, EmailVerificationSerializer
from .utils import make_verification_token, verify_verification_token
from rest_framework.permissions import IsAdminUser
from .serializers import UserSerializer

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token = make_verification_token(user)
        # build verification URL
        verify_path = reverse('api:verify-email')
        scheme = getattr(settings, 'SITE_SCHEME', 'http')
        domain = getattr(settings, 'SITE_DOMAIN', '127.0.0.1:8000')
        verify_url = f"{scheme}://{domain}{verify_path}?token={token}"

        # send email
        subject = 'Verify your email'
        message = f'Hi {user.username},\n\nPlease verify your email by clicking the link below:\n{verify_url}\n\nIf you did not sign up, ignore this email.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'detail': 'Token parameter missing'}, status=status.HTTP_400_BAD_REQUEST)
        data = verify_verification_token(token)
        if not data:
            return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        user_id = data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            return Response({'detail': 'Account already activated'}, status=status.HTTP_200_OK)

        user.is_active = True
        user.save()
        return Response({'detail': 'Email verified. You can now log in.'}, status=status.HTTP_200_OK)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]
