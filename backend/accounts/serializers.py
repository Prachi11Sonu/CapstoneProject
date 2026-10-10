
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "confirm_password",
            "role",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )

        return value.lower()

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })

        if data["role"] == User.Role.ADMIN:
            raise serializers.ValidationError({
                "role": "Admin accounts cannot be created through public registration."
            })

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
