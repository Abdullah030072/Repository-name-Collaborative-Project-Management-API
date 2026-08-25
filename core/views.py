from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

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

from .serializers import (
    UserSerializer,
    ProfileSerializer,
    ProjectSerializer,
    TaskSerializer,
    DocumentSerializer,
    CommentSerializer,
    TimelineEventSerializer,
    NotificationSerializer,
)

from .permissions import (
    IsManager,
    IsCommentAuthorOrReadOnly,
)


# ============================================================
# Ticket 1 - User Registration API
# ============================================================

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


# ============================================================
# Ticket 3 - User Logout API
# ============================================================

class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# ============================================================
# User List API
# ============================================================

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsManager]


# ============================================================
# Profile List + Create API
# ============================================================

class ProfileListAPIView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]

        return [IsAuthenticated()]


# ============================================================
# Profile Detail + Update API
# ============================================================

class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [IsManager()]

        return [IsAuthenticated()]


# ============================================================
# Ticket 4 + 5 - Create/List Projects API
# ============================================================

class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# ============================================================
# Ticket 6 + 7 + 8 - Project Detail/Update/Delete API
# ============================================================

class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsManager()]

        return [IsAuthenticated()]


# ============================================================
# Ticket 9 + 10 - Create/List Tasks API
# ============================================================

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()


# ============================================================
# Ticket 11 + 12 + 13 - Task Detail/Update/Delete API
# ============================================================

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsManager()]

        return [IsAuthenticated()]


# ============================================================
# Ticket 14 - Assign Task API
# ============================================================

class TaskAssignAPIView(generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsManager]

    def post(self, request, pk):
        task = self.get_object()
        assignee_id = request.data.get("assignee")

        if not assignee_id:
            return Response(
                {"detail": "Assignee is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(id=assignee_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not task.project.team_members.filter(id=user.id).exists():
            return Response(
                {"detail": "User is not a member of this project."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.assignee = user
        task.save()

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK,
        )


# ============================================================
# Ticket 15 - Upload Document API
# ============================================================

class DocumentUploadAPIView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsManager]

    def perform_create(self, serializer):
        serializer.save()


# ============================================================
# Ticket 16 - List Documents API
# ============================================================

class DocumentListAPIView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]


# ============================================================
# Ticket 17 + 18 + 19 - Document Detail/Update/Delete API
# ============================================================

class DocumentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsManager()]

        return [IsAuthenticated()]


# ============================================================
# Ticket 20 - Create Comment API
# ============================================================

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ============================================================
# Ticket 21 - List Comments API
# ============================================================

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


# ============================================================
# Ticket 22 + 23 + 24 - Comment Detail/Update/Delete API
# ============================================================

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
        IsCommentAuthorOrReadOnly,
    ]


# ============================================================
# Ticket 25 - List Timeline Events API
# ============================================================

class TimelineEventListAPIView(generics.ListAPIView):
    queryset = TimelineEvent.objects.all().order_by("-created_at")
    serializer_class = TimelineEventSerializer
    permission_classes = [IsAuthenticated]


# ============================================================
# Ticket 26 - Notifications API
# ============================================================

class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


# ============================================================
# Ticket 27 - Mark Notification as Read API
# ============================================================

class NotificationMarkReadAPIView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read"])

        return Response(
            NotificationSerializer(notification).data,
            status=status.HTTP_200_OK,
        )