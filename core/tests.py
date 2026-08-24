from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase
from rest_framework import status

from .models import (
    User,
    Profile,
    Project,
    Task,
    Notification,
    Document,
    Comment,
    TimelineEvent,
)


class UserAuthenticationTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123",
        }

    def test_user_registration(self):
        response = self.client.post(
            "/api/register/",
            self.user_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(username="testuser").exists()
        )

    def test_user_login(self):
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


class ProjectAPITests(APITestCase):

    def setUp(self):
        self.manager = User.objects.create_user(
            username="manager",
            email="manager@example.com",
            password="TestPassword123",
        )

        Profile.objects.create(
            user=self.manager,
            role=Profile.Role.MANAGER,
        )

        self.client.force_authenticate(user=self.manager)

    def test_create_project(self):
        response = self.client.post(
            "/api/projects/",
            {
                "title": "Test Project",
                "description": "Project description",
                "start_date": "2026-08-24",
                "end_date": "2026-09-24",
                "team_members": [],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Project.objects.filter(
                title="Test Project"
            ).exists()
        )

    def test_list_projects(self):
        Project.objects.create(
            title="Project 1",
            description="First project",
            created_by=self.manager,
        )

        Project.objects.create(
            title="Project 2",
            description="Second project",
            created_by=self.manager,
        )

        response = self.client.get("/api/projects/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 2)

    def test_project_detail(self):
        project = Project.objects.create(
            title="Test Project",
            description="Project description",
            created_by=self.manager,
        )

        response = self.client.get(
            f"/api/projects/{project.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Test Project",
        )

    def test_update_project(self):
        project = Project.objects.create(
            title="Old Title",
            description="Old description",
            created_by=self.manager,
        )

        response = self.client.put(
            f"/api/projects/{project.id}/",
            {
                "title": "Updated Title",
                "description": "Updated description",
                "start_date": "2026-08-24",
                "end_date": "2026-09-24",
                "team_members": [],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        project.refresh_from_db()

        self.assertEqual(
            project.title,
            "Updated Title",
        )

    def test_delete_project(self):
        project = Project.objects.create(
            title="Delete Project",
            created_by=self.manager,
        )

        response = self.client.delete(
            f"/api/projects/{project.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Project.objects.filter(
                id=project.id
            ).exists()
        )


class TaskAPITests(APITestCase):

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

        Profile.objects.create(
            user=self.manager,
            role=Profile.Role.MANAGER,
        )

        Profile.objects.create(
            user=self.developer,
            role=Profile.Role.DEVELOPER,
        )

        self.project = Project.objects.create(
            title="Test Project",
            description="Project description",
            created_by=self.manager,
        )

        self.project.team_members.add(self.developer)

        self.client.force_authenticate(
            user=self.manager
        )

    def test_create_task(self):
        response = self.client.post(
            "/api/tasks/",
            {
                "title": "Test Task",
                "description": "Task description",
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

        self.assertTrue(
            Task.objects.filter(
                title="Test Task"
            ).exists()
        )

    def test_list_tasks(self):
        Task.objects.create(
            title="Task 1",
            description="First task",
            project=self.project,
        )

        Task.objects.create(
            title="Task 2",
            description="Second task",
            project=self.project,
        )

        response = self.client.get("/api/tasks/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(len(response.data), 2)

    def test_task_detail(self):
        task = Task.objects.create(
            title="Test Task",
            description="Task description",
            project=self.project,
        )

        response = self.client.get(
            f"/api/tasks/{task.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Test Task",
        )

    def test_update_task(self):
        task = Task.objects.create(
            title="Old Task",
            description="Old description",
            project=self.project,
        )

        response = self.client.put(
            f"/api/tasks/{task.id}/",
            {
                "title": "Updated Task",
                "description": "Updated description",
                "status": "working",
                "project": self.project.id,
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
            task.title,
            "Updated Task",
        )

        self.assertEqual(
            task.status,
            "working",
        )

    def test_delete_task(self):
        task = Task.objects.create(
            title="Delete Task",
            description="Delete me",
            project=self.project,
        )

        response = self.client.delete(
            f"/api/tasks/{task.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Task.objects.filter(
                id=task.id
            ).exists()
        )

    def test_assign_task(self):
        task = Task.objects.create(
            title="Assign Task",
            description="Assign me",
            project=self.project,
        )

        response = self.client.post(
            f"/api/tasks/{task.id}/assign/",
            {
                "assignee": self.developer.id
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

    def test_assign_task_to_non_team_member_fails(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="TestPassword123",
        )

        task = Task.objects.create(
            title="Assign Task",
            description="Assign me",
            project=self.project,
        )

        response = self.client.post(
            f"/api/tasks/{task.id}/assign/",
            {
                "assignee": other_user.id
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        task.refresh_from_db()

        self.assertIsNone(task.assignee)


class DocumentAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="documentuser",
            email="document@example.com",
            password="TestPassword123",
        )

        Profile.objects.create(
            user=self.user,
            role=Profile.Role.DEVELOPER,
        )

        self.project = Project.objects.create(
            title="Document Project",
            description="Project for document testing",
            created_by=self.user,
        )

        self.client.force_authenticate(
            user=self.user
        )

    def create_test_file(self):
        return SimpleUploadedFile(
            "test_document.txt",
            b"This is a test document.",
            content_type="text/plain",
        )

    def test_upload_document(self):
        response = self.client.post(
            "/api/documents/",
            {
                "name": "Test Document",
                "description": "Test document description",
                "file": self.create_test_file(),
                "version": "1.0",
                "project": self.project.id,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Document.objects.filter(
                name="Test Document"
            ).exists()
        )

    def test_list_documents(self):
        Document.objects.create(
            name="Document 1",
            description="First document",
            file=self.create_test_file(),
            version="1.0",
            project=self.project,
        )

        Document.objects.create(
            name="Document 2",
            description="Second document",
            file=self.create_test_file(),
            version="2.0",
            project=self.project,
        )

        response = self.client.get(
            "/api/documents/list/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_document_detail(self):
        document = Document.objects.create(
            name="Test Document",
            description="Test description",
            file=self.create_test_file(),
            version="1.0",
            project=self.project,
        )

        response = self.client.get(
            f"/api/documents/{document.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["name"],
            "Test Document",
        )

    def test_update_document(self):
        document = Document.objects.create(
            name="Old Document",
            description="Old description",
            file=self.create_test_file(),
            version="1.0",
            project=self.project,
        )

        response = self.client.put(
            f"/api/documents/{document.id}/",
            {
                "name": "Updated Document",
                "description": "Updated description",
                "file": self.create_test_file(),
                "version": "2.0",
                "project": self.project.id,
            },
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        document.refresh_from_db()

        self.assertEqual(
            document.name,
            "Updated Document",
        )

        self.assertEqual(
            document.version,
            "2.0",
        )

    def test_delete_document(self):
        document = Document.objects.create(
            name="Delete Document",
            description="Delete me",
            file=self.create_test_file(),
            version="1.0",
            project=self.project,
        )

        response = self.client.delete(
            f"/api/documents/{document.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Document.objects.filter(
                id=document.id
            ).exists()
        )

    def test_document_api_requires_authentication(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(
            "/api/documents/list/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class CommentAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="commentuser",
            email="comment@example.com",
            password="TestPassword123",
        )

        Profile.objects.create(
            user=self.user,
            role=Profile.Role.DEVELOPER,
        )

        self.project = Project.objects.create(
            title="Comment Project",
            description="Project for comment testing",
            created_by=self.user,
        )

        self.task = Task.objects.create(
            title="Comment Task",
            description="Task for comment testing",
            project=self.project,
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_create_comment(self):
        response = self.client.post(
            "/api/comments/",
            {
                "text": "This is a test comment.",
                "task": self.task.id,
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        comment = Comment.objects.get(
            text="This is a test comment."
        )

        self.assertEqual(
            comment.author,
            self.user,
        )

    def test_list_comments(self):
        Comment.objects.create(
            text="Comment 1",
            author=self.user,
            task=self.task,
            project=self.project,
        )

        Comment.objects.create(
            text="Comment 2",
            author=self.user,
            task=self.task,
            project=self.project,
        )

        response = self.client.get(
            "/api/comments/list/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

    def test_comment_detail(self):
        comment = Comment.objects.create(
            text="Test comment",
            author=self.user,
            task=self.task,
            project=self.project,
        )

        response = self.client.get(
            f"/api/comments/{comment.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["text"],
            "Test comment",
        )

    def test_update_own_comment(self):
        comment = Comment.objects.create(
            text="Old comment",
            author=self.user,
            task=self.task,
            project=self.project,
        )

        response = self.client.put(
            f"/api/comments/{comment.id}/",
            {
                "text": "Updated comment",
                "task": self.task.id,
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        comment.refresh_from_db()

        self.assertEqual(
            comment.text,
            "Updated comment",
        )

    def test_delete_own_comment(self):
        comment = Comment.objects.create(
            text="Delete this comment",
            author=self.user,
            task=self.task,
            project=self.project,
        )

        response = self.client.delete(
            f"/api/comments/{comment.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Comment.objects.filter(
                id=comment.id
            ).exists()
        )

    def test_user_cannot_modify_other_users_comment(self):
        other_user = User.objects.create_user(
            username="othercommentuser",
            email="othercomment@example.com",
            password="TestPassword123",
        )

        comment = Comment.objects.create(
            text="Other user's comment",
            author=other_user,
            task=self.task,
            project=self.project,
        )

        response = self.client.put(
            f"/api/comments/{comment.id}/",
            {
                "text": "Trying to modify another user's comment",
                "task": self.task.id,
                "project": self.project.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        response = self.client.delete(
            f"/api/comments/{comment.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        
class NotificationAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="notificationuser",
            email="notification@example.com",
            password="TestPassword123",
        )

        self.other_user = User.objects.create_user(
            username="othernotificationuser",
            email="othernotification@example.com",
            password="TestPassword123",
        )

        Profile.objects.create(
            user=self.user,
            role=Profile.Role.DEVELOPER,
        )

        Profile.objects.create(
            user=self.other_user,
            role=Profile.Role.DEVELOPER,
        )

        self.notification = Notification.objects.create(
            user=self.user,
            message="Test notification",
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_mark_notification_as_read(self):
        response = self.client.put(
            f"/api/notifications/{self.notification.id}/mark_read/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.notification.refresh_from_db()

        self.assertTrue(
            self.notification.is_read
        )

    def test_user_cannot_mark_other_users_notification_as_read(self):
        notification = Notification.objects.create(
            user=self.other_user,
            message="Other user's notification",
        )

        response = self.client.put(
            f"/api/notifications/{notification.id}/mark_read/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        notification.refresh_from_db()

        self.assertFalse(
            notification.is_read
        )

    def test_mark_notification_requires_authentication(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.put(
            f"/api/notifications/{self.notification.id}/mark_read/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )