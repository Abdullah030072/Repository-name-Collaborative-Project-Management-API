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