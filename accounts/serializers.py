from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import LogmanUser
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogmanUser
        fields = ['id', 'email', 'name', 'is_active', 'is_superuser' ,  'organization','password' ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        fields = ['password','organization','name','email']
        for field in fields:
            if not validated_data.get(field):
                print(field)
                raise serializers.ValidationError({field: "This field is required."})
        org = validated_data['organization']
        name = validated_data['name']
        email= validated_data['email']

        user = LogmanUser.objects.create(organization=org, name=name, email=email)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token['name'] = user.name
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user_groups = self.user.groups.values_list('name', flat=True)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'name': self.user.name,
            'groups': list(user_groups)
        }
        return data