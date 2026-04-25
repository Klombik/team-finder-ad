from django.conf import settings
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = (
        (STATUS_OPEN, "Открыт"),
        (STATUS_CLOSED, "Закрыт"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="participating_projects",
    )
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="favorites",
    )
    skills = models.ManyToManyField(Skill, blank=True, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
