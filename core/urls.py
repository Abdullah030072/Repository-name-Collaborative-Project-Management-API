from django.urls import path

from .views import (
    UserRegistrationAPIView,
    UserListAPIView,
    ProfileListAPIView,
    ProfileDetailAPIView,
    ProjectListCreateAPIView,
    ProjectDetailAPIView,
    LogoutAPIView,
    TaskListCreateAPIView,
    TaskDetailAPIView,
    TaskAssignAPIView,
    DocumentUploadAPIView,
    DocumentListAPIView,
    DocumentDetailAPIView,
    CommentCreateAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
    TimelineEventListAPIView,
)


urlpatterns = [
    # Ticket 1 - User Registration
    path(
        "register/",
        UserRegistrationAPIView.as_view(),
        name="register"
    ),

    # Ticket 3 - User Logout
    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout"
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

    # Ticket 9 + Ticket 10 - Task APIs
    path(
        "tasks/",
        TaskListCreateAPIView.as_view(),
        name="task-list-create"
    ),
    
        # Ticket 11 - Task Detail API
    path(
        "tasks/<int:pk>/",
        TaskDetailAPIView.as_view(),
        name="task-detail"
    ),
    
    # Ticket 14 - Assign Task API
path(
    "tasks/<int:pk>/assign/",
    TaskAssignAPIView.as_view(),
    name="task-assign"
),

# Ticket 15 - Upload Document API
path(
    "documents/",
    DocumentUploadAPIView.as_view(),
    name="document-upload"
),

# Ticket 16 - List Documents API
path(
    "documents/list/",
    DocumentListAPIView.as_view(),
    name="document-list"
),

# Ticket 17 - Document Detail API
path(
    "documents/<int:pk>/",
    DocumentDetailAPIView.as_view(),
    name="document-detail"
),
# Ticket 20 - Create Comment API
path(
    "comments/",
    CommentCreateAPIView.as_view(),
    name="comment-create"
),

# Ticket 21 - List Comments API
path(
    "comments/list/",
    CommentListAPIView.as_view(),
    name="comment-list"
),
# Ticket 22 - Comment Detail API
path(
    "comments/<int:pk>/",
    CommentDetailAPIView.as_view(),
    name="comment-detail"
),

# Ticket 25 - List Timeline Events API
path(
    "timeline/",
    TimelineEventListAPIView.as_view(),
    name="timeline-list"
),
]


