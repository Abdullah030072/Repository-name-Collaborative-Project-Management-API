from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from .models import (
    User,
    Profile,
    Project,
    Task,
    Document,
    Comment,
    Notification,
)


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username="manager",
            email="manager@example.com",
            password="TestPassword123",
        )

        self.developer = User.objects.create_user(
            username="developer",
            email="developer@example.com",
            password="TestPassword123",
        )

        self.qa = User.objects.create_user(
            username="qa",
            email="qa@example.com",
            password="TestPassword123",
        )

        Profile.objects.create(
            user=self.manager,
            role=Profile.Role.MANAGER,
        )

        Profile.objects.create(
            user=self.developer,
            role=Profile.Role.DEVELOPER,
        )

        Profile.objects.create(
            user=self.qa,
            role=Profile.Role.QA,
        )

        self.project = Project.objects.create(
            title="Test Project",
            description="Test Description",
            created_by=self.manager,
        )

        self.project.team_members.add(self.developer)

        self.client.force_authenticate(user=self.manager)


# ============================================================
# AUTHENTICATION
# ============================================================

class AuthenticationTests(APITestCase):

    def test_register_user(self):
        response = self.client.post(
            "/api/register/",
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "TestPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_login_user(self):
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123",
        )

        response = self.client.post(
            "/api/login/",
            {
                "username": "testuser",
                "password": "TestPassword123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_login(self):
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="TestPassword123",
        )

        response = self.client.post(
            "/api/login/",
            {
                "username": "testuser",
                "password": "WrongPassword",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


# ============================================================
# PROFILE
# ============================================================

class ProfileTests(BaseAPITestCase):

    def test_manager_can_create_profile(self):
        user = User.objects.create_user(
            username="newdeveloper",
            email="newdeveloper@example.com",
            password="TestPassword123",
        )

        response = self.client.post(
            "/api/profiles/",
            {
                "user": user.id,
                "role": Profile.Role.DEVELOPER,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_authenticated_user_can_view_profile(self):
        profile = self.developer.profile

        response = self.client.get(
            f"/api/profiles/{profile.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_unauthenticated_user_cannot_view_profiles(self):
        self.client.force_authenticate(user=None)

        response = self.client.get("/api/profiles/")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


# ============================================================
# PROJECT
# ============================================================

class ProjectTests(BaseAPITestCase):

    def test_manager_can_create_project(self):
        response = self.client.post(
            "/api/projects/",
            {
                "title": "New Project",
                "description": "Project Description",
                "team_members": [],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_users_can_view_projects(self):
        self.client.force_authenticate(
            user=self.developer
        )

        response = self.client.get("/api/projects/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_manager_can_update_project(self):
        response = self.client.put(
            f"/api/projects/{self.project.id}/",
            {
                "title": "Updated Project",
                "description": "Updated Description",
                "team_members": [],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_developer_cannot_create_project(self):
        self.client.force_authenticate(
            user=self.developer
        )

        response = self.client.post(
            "/api/projects/",
            {
                "title": "Developer Project",
                "description": "Not allowed",
                "team_members": [],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )


# ============================================================
# TASK
# ============================================================

class TaskTests(BaseAPITestCase):

    def create_task(self):
        return Task.objects.create(
            title="Test Task",
            description="Task Description",
            project=self.project,
        )

    def test_manager_can_create_task(self):
        response = self.client.post(
            "/api/tasks/",
            {
                "title": "New Task",
                "description": "Task Description",
                "status": "open",
                "project": self.project.id,
                "assignee": self.developer.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_users_can_view_tasks(self):
        self.create_task()

        self.client.force_authenticate(
            user=self.developer
        )

        response = self.client.get("/api/tasks/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_manager_can_update_task(self):
        task = self.create_task()

        response = self.client.put(
            f"/api/tasks/{task.id}/",
            {
                "title": "Updated Task",
                "description": "Updated",
                "status": "working",
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_developer_cannot_update_task(self):
        task = self.create_task()

        self.client.force_authenticate(
            user=self.developer
        )

        response = self.client.put(
            f"/api/tasks/{task.id}/",
            {
                "title": "Not Allowed",
                "description": "Test",
                "status": "working",
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_manager_can_assign_task(self):
        task = self.create_task()

        response = self.client.post(
            f"/api/tasks/{task.id}/assign/",
            {
                "assignee": self.developer.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        task.refresh_from_db()

        self.assertEqual(
            task.assignee,
            self.developer,
        )


# ============================================================
# DOCUMENT
# ============================================================

class DocumentTests(BaseAPITestCase):

    def create_file(self):
        return SimpleUploadedFile(
            "test.txt",
            b"Test document",
            content_type="text/plain",
        )

    def create_document(self):
        return Document.objects.create(
            name="Test Document",
            description="Test Description",
            file=self.create_file(),
            version="1.0",
            project=self.project,
        )

    def test_manager_can_upload_document(self):
        response = self.client.post(
            "/api/documents/",
            {
                "name": "Test Document",
                "description": "Test Description",
                "file": self.create_file(),
                "version": "1.0",
                "project": self.project.id,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_user_can_list_documents(self):
        self.create_document()

        response = self.client.get(
            "/api/documents/list/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_user_can_delete_document(self):
        document = self.create_document()

        response = self.client.delete(
            f"/api/documents/{document.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )


# ============================================================
# COMMENTS
# ============================================================

class CommentTests(BaseAPITestCase):

    def create_comment(self):
        task = Task.objects.create(
            title="Comment Task",
            project=self.project,
        )

        return Comment.objects.create(
            text="Test Comment",
            author=self.developer,
            task=task,
            project=self.project,
        )

    def test_user_can_create_comment(self):
        self.client.force_authenticate(
            user=self.developer
        )

        response = self.client.post(
            "/api/comments/",
            {
                "text": "New Comment",
                "task": self.create_comment().task.id,
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_user_can_view_other_users_comment(self):
        comment = self.create_comment()

        response = self.client.get(
            f"/api/comments/{comment.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_user_cannot_update_other_users_comment(self):
        comment = self.create_comment()

        response = self.client.put(
            f"/api/comments/{comment.id}/",
            {
                "text": "Trying to edit",
                "task": comment.task.id,
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )


# ============================================================
# NOTIFICATIONS
# ============================================================

class NotificationTests(BaseAPITestCase):

    def setUp(self):
        super().setUp()

        self.notification = Notification.objects.create(
            user=self.manager,
            message="Test notification",
        )

    def test_user_can_view_own_notifications(self):
        response = self.client.get(
            "/api/notifications/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_user_can_mark_notification_as_read(self):
        response = self.client.put(
            f"/api/notifications/"
            f"{self.notification.id}/mark_read/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.notification.refresh_from_db()

        self.assertTrue(
            self.notification.is_read
        )

    def test_user_cannot_mark_other_users_notification(self):
        notification = Notification.objects.create(
            user=self.developer,
            message="Private notification",
        )

        response = self.client.put(
            f"/api/notifications/"
            f"{notification.id}/mark_read/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )


# ============================================================
# TIMELINE
# ============================================================

class TimelineTests(BaseAPITestCase):

    def test_authenticated_user_can_view_timeline(self):
        response = self.client.get(
            "/api/timeline/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_unauthenticated_user_cannot_view_timeline(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(
            "/api/timeline/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )