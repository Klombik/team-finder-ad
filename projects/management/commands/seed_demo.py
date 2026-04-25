from django.core.management.base import BaseCommand

from projects.models import Project, Skill
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_data = [
            ("anna@example.com", "Анна", "Смирнова", "Frontend-разработчик", "+79990000001"),
            ("ivan@example.com", "Иван", "Петров", "Backend-разработчик", "+79990000002"),
            ("maria@example.com", "Мария", "Иванова", "UI/UX-дизайнер", "+79990000003"),
        ]
        users = []
        for email, name, surname, about, phone in users_data:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"name": name, "surname": surname, "about": about, "phone": phone},
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        skill_names = ["Django", "React", "PostgreSQL", "Docker", "Figma"]
        skills = {name: Skill.objects.get_or_create(name=name)[0] for name in skill_names}

        projects_data = [
            (users[0], "Платформа для поиска команды", "Сервис для поиска участников в учебные проекты."),
            (users[1], "API для задач", "Backend для трекера задач с ролями и статусами."),
            (users[2], "Дизайн-система", "Набор компонентов и правил для единого интерфейса."),
        ]
        for owner, name, description in projects_data:
            project, _ = Project.objects.get_or_create(
                owner=owner,
                name=name,
                defaults={"description": description, "github_url": "https://github.com/"},
            )
            project.skills.add(skills["Django"], skills["Docker"])
            for user in users:
                if user != owner:
                    project.participants.add(user)

        projects = list(Project.objects.all())
        if projects:
            users[0].favorites.add(projects[-1])
            users[1].favorites.add(projects[0])

        self.stdout.write(self.style.SUCCESS("Demo data is ready"))
