from django.urls import path

from .views import (
    UserListAPIView,
    ProfileListAPIView,
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
)

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('profiles/', ProfileListAPIView.as_view(), name='profile-list'),

    path(
        'projects/',
        ProjectListCreateAPIView.as_view(),
        name='project-list-create'
    ),

    path(
        'projects/<int:pk>/',
        ProjectDetailAPIView.as_view(),
        name='project-detail'
    ),
]