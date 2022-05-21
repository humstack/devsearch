from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import Project, Tag


def search_projects(request):
    search_query = ""
    project_list = None

    if request.GET.get('search_field'):
        search_query = request.GET.get('search_field')

        tag_list = Tag.objects.filter(
            Q(name__icontains=search_query)
        )

        project_list = Project.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(owner__name__icontains=search_query) |
            Q(tags__in=tag_list)
        )

    else:
        project_list = Project.objects.all()

    return project_list, search_query


def paginate_projects(request, projects):
    results = 3
    page = 1
    projects = list(projects)
    paginator = Paginator(projects, results)

    try:
        page = request.GET.get('page', page)

        project_list = paginator.page(page)

    except EmptyPage:
        messages.error(request, "That page does not exist")
        page = 1
        project_list = paginator.page(page)

    except PageNotAnInteger:
        messages.error(request, "That page is invalid.")
        page = 1
        project_list = paginator.page(page)

    left_index = (int(page) - 4)

    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return project_list, custom_range
