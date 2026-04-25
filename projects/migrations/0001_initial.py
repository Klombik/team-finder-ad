import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Skill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("github_url", models.URLField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("open", "Открыт"), ("closed", "Закрыт")],
                        default="open",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owned_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        blank=True,
                        related_name="participating_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "liked_by",
                    models.ManyToManyField(
                        blank=True,
                        related_name="favorites",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "skills",
                    models.ManyToManyField(blank=True, related_name="projects", to="projects.skill"),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
