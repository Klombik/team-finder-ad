from django.core.management.base import BaseCommand

from projects.models import Project, Skill
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_data = [
            (
                "dev_alex@example.com",
                "Алексей",
                "Морозов",
                "Fullstack-разработчик",
                "+79991110001",
            ),
            (
                "teamcoder@example.com",
                "Максим",
                "Волков",
                "Python-разработчик",
                "+79991110002",
            ),
            (
                "design_lena@example.com",
                "Елена",
                "Кузнецова",
                "Дизайнер интерфейсов",
                "+79991110003",
            ),
        ]

        users = []
        for email, name, surname, about, phone in users_data:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "name": name,
                    "surname": surname,
                    "about": about,
                    "phone": phone,
                },
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        skill_names = [
            "Django",
            "React",
            "PostgreSQL",
            "Docker",
            "Figma",
            "Python",
            "TypeScript",
        ]
        skills = {name: Skill.objects.get_or_create(name=name)[0] for name in skill_names}

        projects_data = [
            (
                users[0],
                "Сервис подбора команды",
                "Приложение для поиска людей в учебные и pet-проекты.",
            ),
            (
                users[1],
                "Планировщик командных задач",
                "Backend-сервис для управления задачами, ролями и участниками.",
            ),
            (
                users[2],
                "UI-kit для веб-приложений",
                "Набор визуальных компонентов для единого оформления страниц.",
            ),
        ]

        for owner, name, description in projects_data:
            project, _ = Project.objects.get_or_create(
                owner=owner,
                name=name,
                defaults={
                    "description": description,
                    "github_url": "https://github.com/",
                },
            )
            project.skills.add(skills["Django"], skills["Docker"])
            for user in users:
                if user != owner:
                    project.participants.add(user)

        projects = list(Project.objects.all())
        if projects:
            users[0].favorites.add(projects[-1])
            users[1].favorites.add(projects[0])

        self.stdout.write(self.style.SUCCESS("Демонстрационные данные добавлены"))