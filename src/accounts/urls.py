from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import RegisterAPIView, UserAPIView

router = DefaultRouter()
router.register(r'users', UserAPIView, basename='user')

urlpatterns = [
    # Define your account-related URLs here
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),  # Token authentication endpoint
    path('register/', RegisterAPIView.as_view(), name='register'),  # User registration endpoint
]