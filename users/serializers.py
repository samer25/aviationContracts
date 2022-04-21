from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

# from board.serializers import SeekerProfileSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name', 'password']


class CustomUserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name', 'profile']
