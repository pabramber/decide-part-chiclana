from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(label="Enter username")
    password = serializers.CharField(label="Enter your password")
    first_name = serializers.CharField(label="Enter first name")
    last_name = serializers.CharField(label="Enter last name")
    email = serializers.EmailField(label="Enter email")
    is_staff = serializers.BooleanField(label="Enter if this user is staff")
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Enter username")
    password = serializers.CharField(label="Enter your password")
