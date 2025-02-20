from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import BasicProblem, DotProductProblem, UserProgress


class BasicProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicProblem
        fields = "__all__"


class DotProductProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DotProductProblem
        fields = "__all__"


class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = "__all__"


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}  # Hide password in responses
