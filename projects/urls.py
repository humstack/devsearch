from django.urls import path
from . import views as project_views


urlpatterns = [
    path("", project_views.projects, name="projects"),
    path("create-project/", project_views.create_project, name="create-project"),
    path("<str:pk>/", project_views.get_project, name="get-project"),
    path("update-project/<str:pk>/", project_views.update_project, name="update-project"),
    path("delete-project/<str:pk>/", project_views.delete_project, name="delete-project"),
]
