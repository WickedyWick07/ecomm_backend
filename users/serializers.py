from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'username', 'password', 'email', 'first_name', 'last_name']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError('Invalid username or password')

            if not user.check_password(password):
                raise serializers.ValidationError('Invalid username or password')

            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')

            data['user'] = user
        else:
            raise serializers.ValidationError('Both "username" and "password" are required.')

        return data