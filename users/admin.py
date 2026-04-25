from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ["email"]
    list_display = ["email", "name", "surname", "is_staff", "created_at"]
    search_fields = ["email", "name", "surname"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Профиль", {"fields": ("name", "surname", "about", "phone", "github_url", "avatar")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "name", "surname", "password1", "password2")}),
    )
