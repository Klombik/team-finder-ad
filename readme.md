# Team Finder

Team Finder — Django-приложение для поиска участников в проекты.

## Запуск

```bash
cp .env_example .env
docker compose up --build
```

Сайт будет доступен по адресу:

```text
http://localhost:8000
```

## Админ-панель

```bash
docker compose exec web python manage.py createsuperuser
```

Админ-панель:

```text
http://localhost:8000/admin/
```

## Тестовые данные

Тестовые пользователи и проекты создаются автоматически при запуске контейнера командой `seed_demo`.

Данные для входа:

```text
anna@example.com / password123
ivan@example.com / password123
maria@example.com / password123
```

## Полезные команды

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_demo
docker compose exec web flake8
```

## Остановка

```bash
docker compose down
```

Чтобы удалить базу вместе с volume:

```bash
docker compose down -v
```
