from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
        min_length=6
    )
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def validate_email_unique(self, email):
        """Check that provided email isn't already used"""
        if email and User.objects.filter(email__exact=email).exists():
            raise serializers.ValidationError("This email is already used by different account")
        # You need to return the value in after validation.
        return email

    def create(self, validated_data):
        validated_data["email"] = self.validate_email_unique(validated_data.get("email"))
        validated_data["password"] = make_password(validated_data.get("password"))
        return super().create(validated_data)
