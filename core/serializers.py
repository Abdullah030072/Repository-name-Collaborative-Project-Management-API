from rest_framework import serializers

from .models import User, Profile, Project


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "profile_picture",
            "role",
            "contact_number",
        ]
        read_only_fields = ["id"]


# Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_by",
            "created_at",
            "updated_at",
        ]