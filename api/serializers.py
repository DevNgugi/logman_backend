from rest_framework import serializers
from .models import Organization, Source,Connection
from api.utils.crypt import cipher_suite
from api.utils.generators import generate_code

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'



class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['ssh_user','ssh_host','ssh_port']


    def create(self, validated_data):
        _fields = ['ssh_user','ssh_host','ssh_port']
        for field in _fields:
            if not validated_data.get(field):
                raise serializers.ValidationError({field: "This field is required."})
        username = validated_data['ssh_user']
        port = validated_data['ssh_port']
        host = validated_data['ssh_host']

        ssh_pass = validated_data.pop('ssh_pass', None)
        if ssh_pass is None:
            raise serializers.ValidationError({'ssh_pass': 'ssh password is required.'})
        


        try:
            password = cipher_suite().encrypt(password.encode())

        except Exception as e:
            raise serializers.ValidationError(f"Error encoding password to binary: {str(e)}")

        conn = Connection.objects.create(ssh_user=username, ssh_port=port, ssh_pass=password, ssh_host=host)
        conn.save()
        return conn
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['title','code']
        extra_kwargs = {
            'code': {'read_only': True},
        }
    
    def create(self, validated_data):
        validated_data['code'] = generate_code(8)
        return Organization.objects.create(**validated_data)