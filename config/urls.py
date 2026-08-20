"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path,include

from core.views import (
    UserRegistrationAPIView,
    UserListAPIView,
    ProfileListAPIView,
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),

    # Ticket 1 - User Registration
    path(
        'api/register/',
        UserRegistrationAPIView.as_view(),
        name='register'
    ),

    # User APIs
    path(
        'api/users/',
        UserListAPIView.as_view(),
        name='user-list'
    ),

    path(
        'api/profiles/',
        ProfileListAPIView.as_view(),
        name='profile-list'
    ),

    # Project APIs
    path(
        'api/projects/',
        ProjectListCreateAPIView.as_view(),
        name='project-list-create'
    ),

    path(
        'api/projects/<int:pk>/',
        ProjectDetailAPIView.as_view(),
        name='project-detail'
    ),
]