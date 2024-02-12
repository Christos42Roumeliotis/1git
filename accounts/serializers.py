from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length = 4, write_only=True)
    
    class Meta:
        model = User
        fields=['username', 'password']

    def validate(self,attrs):
        username = attrs.get('username','')
        if not username.isalnum():
            raise serializers.ValidationError('Username should only contain alphanumerical characters')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type':'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user']=user
        return attrs