from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render

from projects.models import Project
from team_finder.utils import paginate_queryset

from .forms import EmailLoginForm, ProfileForm, RegisterForm
from .models import User

USERS_PER_PAGE = 12
FILTER_OWNERS_OF_FAVORITES = "owners-of-favorite-projects"
FILTER_OWNERS_OF_PARTICIPATING = "owners-of-participating-projects"
FILTER_INTERESTED_IN_MY_PROJECTS = "interested-in-my-projects"
FILTER_PARTICIPANTS_OF_MY_PROJECTS = "participants-of-my-projects"


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:login")
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    form = EmailLoginForm(request, request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get("next") or "projects:list")
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:list")


def user_detail(request, pk):
    profile = get_object_or_404(User.objects.prefetch_related("owned_projects"), pk=pk)
    return render(request, "users/user-details.html", {"user": profile})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:detail", pk=request.user.pk)
    return render(request, "users/edit_profile.html", {"form": form, "user": request.user})


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect("users:detail", pk=request.user.pk)
    return render(request, "users/change_password.html", {"form": form})


def apply_user_filter(users, current_user, active_filter):
    if active_filter == FILTER_OWNERS_OF_FAVORITES:
        favorite_owner_ids = current_user.favorites.values_list("owner_id", flat=True)
        return users.filter(id__in=favorite_owner_ids)
    if active_filter == FILTER_OWNERS_OF_PARTICIPATING:
        owner_ids = Project.objects.filter(participants=current_user).values_list("owner_id", flat=True)
        return users.filter(id__in=owner_ids)
    if active_filter == FILTER_INTERESTED_IN_MY_PROJECTS:
        admirer_ids = User.objects.filter(favorites__owner=current_user).values_list("id", flat=True)
        return users.filter(id__in=admirer_ids)
    if active_filter == FILTER_PARTICIPANTS_OF_MY_PROJECTS:
        member_ids = User.objects.filter(participating_projects__owner=current_user).values_list(
            "id", flat=True
        )
        return users.filter(id__in=member_ids)
    return users


def user_list(request):
    users = User.objects.all().order_by("-created_at")
    active_filter = request.GET.get("filter")

    if request.user.is_authenticated and active_filter:
        users = apply_user_filter(users, request.user, active_filter)

    selected_skill = request.GET.get("skill")
    if selected_skill:
        users = users.filter(skills__name=selected_skill)

    page = paginate_queryset(request, users.distinct(), USERS_PER_PAGE)
    return render(
        request,
        "users/participants.html",
        {
            "participants": page,
            "page_obj": page,
            "active_filter": active_filter,
            "active_skill": selected_skill,
        },
    )
