from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView, UserListView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'api'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user-list'),
]
