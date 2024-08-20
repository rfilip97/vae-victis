from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username)

                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")

                user = authenticate(username=username, password=password)
                if user is None:
                    raise serializers.ValidationError("Invalid login credentials.")

            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid login credentials.")
        else:
            raise serializers.ValidationError(
                "Must include both username and password."
            )

        data["user"] = user

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2", "email"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(**validated_data)

        return user
