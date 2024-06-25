from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import LogmanUser

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = LogmanUser
        fields = ('id', 'email', 'name', 'password','organization')
        
    def validate(self, attrs):
        if 'organization' not in attrs or attrs['organization'] is None:
            raise serializers.ValidationError("The organization field must be set.")
        return attrs

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = LogmanUser
        fields = ('id', 'email', 'name', 'is_active','organization')
