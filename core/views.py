from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Profile, Project, Task, Document
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    ProjectSerializer,
    TaskSerializer,
    DocumentSerializer, 
)
from .permissions import IsManager


# Ticket 1 - User Registration API
class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# Ticket 3 - User Logout API
class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )


# User List API
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# Profile List + Create API
class ProfileListAPIView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]


# Profile Detail + Update API
class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]


# Ticket 4 - Create Project API
# Ticket 5 - List Projects API
class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# Ticket 6 - Project Detail API
# Ticket 7 - Update Project API
# Ticket 8 - Delete Project API
class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsManager()]

        return [IsAuthenticated()]


# Ticket 9 - Create Task API
# Ticket 10 - List Tasks API
class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()
        
# Ticket 11 - Task Detail API
# Ticket 12 - Update Task API
# Ticket 13 - Delete Task API
class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == "PUT":
            return [IsManager()]

        if self.request.method == "DELETE":
            return [IsManager()]
        
        if self.request.method == "PATCH":
            return [IsManager()]

        return [IsAuthenticated()]
    
# Ticket 14 - Assign Task API
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
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=assignee_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not task.project.team_members.filter(id=user.id).exists():
            return Response(
                {"detail": "User is not a member of this project."},
                status=status.HTTP_400_BAD_REQUEST
            )

        task.assignee = user
        task.save()

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK
        )


# Ticket 15 - Upload Document API
class DocumentUploadAPIView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()      
        
        
# Ticket 16 - List Documents API
class DocumentListAPIView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

# Ticket 17 - Document Detail API
# Ticket 18 - Update Document API
class DocumentDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    