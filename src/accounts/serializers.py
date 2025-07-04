from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterSerializer(ModelSerializer):
    """
    Serializer for user registration.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'last_login', 'date_joined')
        extra_kwargs = {
            'password' : {'write_only' : True,}
        }
        
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        request = self.context.get('request')

        if request and (request.user.is_staff or instance == request.user):
            return representation
        return {
            'id' : representation.get('id'),
            'username' : representation.get('username'),
            'first_name' : representation.get('first_name'),
            'last_name' : representation.get('last_name'),
            'email' : representation.get('email'),
        }