from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2', 'department', 'role')

    def validate(self, attrs):
        # Check if both passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

         # Optionally, validate department and role if needed
        if 'department' not in attrs:
            raise serializers.ValidationError({"department": "This field is required."})
        if 'role' not in attrs:
            raise serializers.ValidationError({"role": "This field is required."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            department = validated_data['department'],
            role = validated_data['role'],
        )
        # Set the password to the provided one
        user.set_password(validated_data['password'])
        user.save()
        return user
