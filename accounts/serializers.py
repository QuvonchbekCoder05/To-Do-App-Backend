from rest_framework import serializers
from .models import User, OTP

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save() 
        return user

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwMjE2MzMyLCJpYXQiOjE3MzAyMTYwMzIsImp0aSI6IjVmNTA0ZmU0NDY4NjQ2Y2M5MGFjYTYzMWQ3MmEzMzRjIiwidXNlcl9pZCI6MX0.c3JuDSk8SH6jEswQjD13H0901jM8DDzfidqLqCnPcR8
