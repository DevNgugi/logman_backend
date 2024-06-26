from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import LogmanUser
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