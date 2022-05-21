from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError

from .models import Project
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, paginate_projects

# Create your views here.


def projects(request):

    project_list, search_query = search_projects(request)

    project_list, custom_range = paginate_projects(request, project_list)

    context = {
        'projects': project_list,
        'search_query': search_query,
        'custom_range': custom_range,
    }

    return render(request, "projects/projects.html", context)


def get_project(request, pk):
    project_obj = Project.objects.get(id=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            try:
                review = form.save(commit=False)

                review.project = project_obj
                review.owner = request.user.profile
                review.save()

            except IntegrityError:
                messages.error(request, "You cannot submit another review for the same project")

            else:
                messages.success(request, "Review submitted successfully.")

                project_obj.get_vote_count()
            finally:
                return redirect("get-project", pk=project_obj.id)

    else:
        form = ReviewForm()

    context = {
        'project': project_obj,
        'form': form,
    }

    return render(request, "projects/single-project.html", context)


@login_required(login_url="login")
def create_project(request):
    user_profile = request.user.profile

    title = "Create Project"

    if request.POST:
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)

            project.owner = user_profile

            project.save()

            messages.success(request, "Project created successfully.")

            return redirect("account")
    else:
        form = ProjectForm()

    context = {
        'form': form,
        'title': title,
    }

    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def update_project(request, pk):
    user_profile = request.user.profile

    project = user_profile.project_set.get(id=pk)

    title = "Edit Project"

    if request.POST:
        form = ProjectForm(request.POST, request.FILES, instance=project)

        if form.is_valid():
            form.save()

            messages.success(request, "Project edited successfully.")

            return redirect("account")
    else:
        form = ProjectForm(instance=project)

    context = {
        'form': form,
        'title': title,
    }

    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    user_profile = request.user.profile

    project = user_profile.project_set.get(id=pk)
    title = "Delete Project"

    if request.POST:
        project.delete()

        messages.success(request, "Project deleted successfully.")

        return redirect("account")

    context = {
        'object': project,
        'title': title,
    }

    return render(request, "delete_template.html", context)
