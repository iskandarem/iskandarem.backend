

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import *
from .permissions import *


class RegisterAPIView(APIView):
    """
    View for user registration.
    """
    serializer_class = RegisterSerializer 
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': {
                    'username': user.username,
                    'email': user.email
                },
                'token': token.key
            }, status=201)
        return Response(serializer.errors, status=400)
    

class UserAPIView(ModelViewSet):
    """
    API view for user operations.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]