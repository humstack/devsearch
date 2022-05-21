from django.urls import path
from . import views as user_views


urlpatterns = [
    path("login/", user_views.login_user, name="login"),
    path("logout/", user_views.logout_user, name="logout"),
    path("register/", user_views.register_user, name="register"),

    path("inbox/", user_views.inbox, name="inbox"),
    path("view-message/<uuid:pk>/", user_views.view_message, name="view-message"),
    path("send-message/<uuid:pk>/", user_views.send_message, name="send-message"),

    path("", user_views.profiles, name="profiles"),
    path("<uuid:pk>/", user_views.profile, name="profile"),

    path("account/", user_views.user_account, name="account"),
    path("edit-account/", user_views.edit_account, name="edit-account"),

    path("create-skill/", user_views.create_skill, name="create-skill"),
    path("update-skill/<uuid:pk>/", user_views.update_skill, name="update-skill"),
    path("delete-skill/<uuid:pk>/", user_views.delete_skill, name="delete-skill"),
]

