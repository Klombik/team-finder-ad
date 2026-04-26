import json
from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from team_finder.utils import paginate_queryset

from .forms import ProjectForm
from .models import Project, Skill

PROJECTS_PER_PAGE = 12
SKILLS_SEARCH_LIMIT = 10


def project_list(request):
    projects = Project.objects.select_related("owner").prefetch_related("participants", "liked_by")
    active_skill = request.GET.get("skill")
    if active_skill:
        projects = projects.filter(skills__name=active_skill)
    page = paginate_queryset(request, projects.distinct(), PROJECTS_PER_PAGE)
    return render(
        request,
        "projects/project_list.html",
        {
            "projects": page,
            "page_obj": page,
            "active_skill": active_skill,
            "all_skills": Skill.objects.values_list("name", flat=True),
        },
    )


def project_detail(request, pk):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants", "skills"),
        pk=pk,
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        return redirect("projects:detail", pk=project.pk)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": False})


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("projects:detail", pk=project.pk)
    return render(request, "projects/create-project.html", {"form": form, "is_edit": True})


@login_required
def favorites(request):
    projects = request.user.favorites.select_related("owner").prefetch_related("participants")
    return render(request, "projects/favorite_projects.html", {"projects": projects})


@login_required
@require_POST
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.liked_by.filter(pk=request.user.pk).exists():
        project.liked_by.remove(request.user)
        value = False
    else:
        project.liked_by.add(request.user)
        value = True
    return JsonResponse({"status": "ok", "favorite": value})


@login_required
@require_POST
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner_id == request.user.id:
        return JsonResponse({"status": "error"}, status=HTTPStatus.FORBIDDEN)
    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
        participant = False
    else:
        project.participants.add(request.user)
        participant = True
    return JsonResponse({"status": "ok", "participant": participant})


@login_required
@require_POST
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    project.status = Project.STATUS_CLOSED
    project.save(update_fields=["status", "updated_at"])
    return JsonResponse({"status": "ok"})


@require_GET
def skills_search(request):
    query = request.GET.get("q", "").strip()
    skills = Skill.objects.all()
    if query:
        skills = skills.filter(name__icontains=query)
    return JsonResponse(list(skills.values("id", "name")[:SKILLS_SEARCH_LIMIT]), safe=False)


@login_required
@require_POST
def add_project_skill(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    payload = json.loads(request.body or "{}")
    skill_id = payload.get("skill_id")
    name = str(payload.get("name", "")).strip()
    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif name:
        skill, _ = Skill.objects.get_or_create(name=name)
    else:
        return JsonResponse({"error": "empty"}, status=HTTPStatus.BAD_REQUEST)
    project.skills.add(skill)
    return JsonResponse({"id": skill.id, "name": skill.name})


@login_required
@require_POST
def remove_project_skill(request, pk, skill_id):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    project.skills.remove(skill_id)
    return JsonResponse({"status": "ok"})
