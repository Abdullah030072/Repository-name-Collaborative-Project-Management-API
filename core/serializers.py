from rest_framework import serializers

from .models import (
    User,
    Profile,
    Project,
    Task,
    Document,
    Comment,
    TimelineEvent,
    Notification,
)


# ============================================================
# User Serializer
# ============================================================

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
        read_only_fields = [
            "id",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


# ============================================================
# Profile Serializer
# ============================================================

class ProfileSerializer(serializers.ModelSerializer):

    # User is accepted as an ID when creating/updating a profile.
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True
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

        read_only_fields = [
            "id",
        ]


# ============================================================
# Project Serializer
# ============================================================

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


# ============================================================
# Task Serializer
# ============================================================

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task

        fields = [
            "id",
            "title",
            "description",
            "status",
            "project",
            "assignee",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# Document Serializer
# ============================================================

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document

        fields = [
            "id",
            "name",
            "description",
            "file",
            "version",
            "project",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# ============================================================
# Comment Serializer
# ============================================================

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment

        fields = [
            "id",
            "text",
            "author",
            "created_at",
            "task",
            "project",
        ]

        read_only_fields = [
            "id",
            "author",
            "created_at",
        ]


# ============================================================
# Timeline Event Serializer
# ============================================================

class TimelineEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimelineEvent

        fields = [
            "id",
            "project",
            "event_type",
            "description",
            "created_by",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_at",
        ]


# ============================================================
# Notification Serializer
# ============================================================

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification

        fields = [
            "id",
            "user",
            "message",
            "created_at",
            "is_read",
        ]

        read_only_fields = [
            "id",
            "user",
            "message",
            "created_at",
            "is_read",
        ]