from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, 
        trim_whitespace=False
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "error": "Invalid email or password. Please try again."
            })

        # Authenticate user by checking the password
        if not user.check_password(password):
            raise serializers.ValidationError({
                "error": "Invalid email or password. Please try again."
            })

        data['user'] = user
        return data
