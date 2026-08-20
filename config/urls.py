from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.views import (
    UserRegistrationAPIView,
    UserListAPIView,
    ProfileListAPIView,
    ProfileDetailAPIView,
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'api/register/',
        UserRegistrationAPIView.as_view(),
        name='register'
    ),

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

    path(
        'api/profiles/<int:pk>/',
        ProfileDetailAPIView.as_view(),
        name='profile-detail'
    ),

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

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )