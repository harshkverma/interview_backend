from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

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
            print(f"Email '{email}' does not exist in the database.")
            raise serializers.ValidationError({
                "error": "Invalid email or password. Please try again."
            })

        if not user.check_password(password):
            print(f"Password mismatch for user '{email}'.")
            raise serializers.ValidationError({
                "error": "Invalid email or password. Please try again."
            })

        print(f"Login successful for user '{email}'.")
        data['user'] = user
        return data



class RegistrationSerializer(serializers.ModelSerializer):
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
