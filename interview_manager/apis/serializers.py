from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Interview, Roles
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

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
        
         # validate department and role if needed
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


    
class InterviewSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()

    class Meta:
        model = Interview
        fields = "__all__"

    def to_internal_value(self, data):
        phone = data.get('phone')

        if isinstance(phone, int):
            raise serializers.ValidationError({
                "phone": "Phone number must be provided as a string, not an integer."
            })

        return super().to_internal_value(data)

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only numeric digits.")

        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")

        return value

    def validate_email(self, value):
        email_validator = EmailValidator()
        try:
            email_validator(value)  # Validate email
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        return value
    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['id', 'job_title']