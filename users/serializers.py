from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super().create(validated_data)
