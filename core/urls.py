from django.urls import path

from .views import (
    UserRegistrationAPIView,
    UserListAPIView,
    ProfileListAPIView,
    ProfileDetailAPIView,
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
)


urlpatterns = [

    # Ticket 1 - User Registration
    path(
        "register/",
        UserRegistrationAPIView.as_view(),
        name="register"
    ),

    # User APIs
    path(
        "users/",
        UserListAPIView.as_view(),
        name="user-list"
    ),

    # Profile APIs
    path(
        "profiles/",
        ProfileListAPIView.as_view(),
        name="profile-list"
    ),

    path(
        "profiles/<int:pk>/",
        ProfileDetailAPIView.as_view(),
        name="profile-detail"
    ),

    # Project APIs
    path(
        "projects/",
        ProjectListCreateAPIView.as_view(),
        name="project-list-create"
    ),

    path(
        "projects/<int:pk>/",
        ProjectDetailAPIView.as_view(),
        name="project-detail"
    ),
]