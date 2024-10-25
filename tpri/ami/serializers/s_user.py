from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from ..models import PowerUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'phone')
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            phone=validated_data.get('phone', '')
        )
        return user

class PowerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = PowerUser
        fields = ['account', 'electricnumber','registered','regdate']


class PowerUserInfoSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=10)

