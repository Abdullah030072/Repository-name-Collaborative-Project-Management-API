from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Profile(models.Model):

    class Role(models.TextChoices):
        MANAGER = 'manager', 'Manager'
        QA = 'qa', 'QA'
        DEVELOPER = 'developer', 'Developer'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    profile_picture = models.ImageField(
        upload_to='',
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DEVELOPER
    )

    contact_number = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_projects'
    )

    team_members = models.ManyToManyField(
        User,
        related_name='team_projects',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Task(models.Model):

    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        REVIEW = 'review', 'Review'
        WORKING = 'working', 'Working'
        AWAITING_RELEASE = 'awaiting_release', 'Awaiting Release'
        WAITING_QA = 'waiting_qa', 'Waiting QA'

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.OPEN
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Document(models.Model):
    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    file = models.FileField(
        upload_to='documents/'
    )

    version = models.CharField(
        max_length=50,
        default='1.0'
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name 
