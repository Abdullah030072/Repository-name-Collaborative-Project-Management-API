from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    #Ticket 1 - User Registration and Authentication APIs
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
    
    # JWT Authentication APIs
path(
    'api/login/',
    TokenObtainPairView.as_view(),
    name='token_obtain_pair'
),

path(
    'api/token/refresh/',
    TokenRefreshView.as_view(),
    name='token_refresh'
),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )