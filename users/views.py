from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import search_profiles, paginate_profiles
# Create your views here.


def login_user(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":

        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect(request.GET['next'] if 'next' in request.GET else "profiles")
            else:
                messages.error(request, "Username OR password incorrect!")

    return render(request, "users/login_register.html", {"page": page})


@login_required(login_url="login")
def logout_user(request):
    logout(request)

    messages.info(request, "User was logged out")

    return redirect("login")


def register_user(request):
    page = "register"

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.username = user.username.lower()
            user.save()

            messages.success(request, "Account created successfully.")

            login(request, user)

            return redirect("account")

        else:
            messages.success(request, "An error has occurred during registration.")

    else:
        form = CustomUserCreationForm()

    context = {
        "page": page,
        "form": form,
    }
    return render(request, "users/login_register.html", context)


def profiles(request):
    profile_list, search_query = search_profiles(request)

    profile_list, custom_range = paginate_profiles(request, profile_list)

    context = {
        'profiles': profile_list,
        'search_query': search_query,
        'custom_range': custom_range,
    }

    return render(request, "users/profiles.html", context)


def profile(request, pk):
    user_profile = Profile.objects.get(pk=pk)

    top_skills = user_profile.skill_set.exclude(description__exact="")
    other_skills = user_profile.skill_set.filter(description__exact="")

    context = {
        'profile': user_profile,
        'top_skills': top_skills,
        'other_skills': other_skills,
    }

    return render(request, "users/profile.html", context)


@login_required(login_url="login")
def user_account(request):
    user_profile = request.user.profile

    skills = user_profile.skill_set.all()
    user_projects = user_profile.project_set.all()

    context = {
        'profile': user_profile,
        'skills': skills,
        'projects': user_projects,
    }

    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_account(request):

    user_profile = request.user.profile

    title = "Edit Account"

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()

            messages.success(request, "Profile edited successfully.")

            return redirect("account")

    else:
        form = ProfileForm(instance=user_profile)

    context = {
        "form": form,
        "title": title,
    }

    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def create_skill(request):

    user_profile = request.user.profile
    title = "Create Skill"

    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = user_profile
            skill.save()

            messages.success(request, "Skill created successfully.")

            return redirect("account")

    else:
        form = SkillForm()

    context = {
        'title': title,
        'form': form,
    }

    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def update_skill(request, pk):

    user_profile = request.user.profile
    user_skill = user_profile.skill_set.get(id=pk)
    title = "Edit Skill"

    if request.method == "POST":
        form = SkillForm(request.POST, instance=user_skill)

        if form.is_valid():
            form.save()

            messages.success(request, "Skill edited successfully.")

            return redirect("account")

    else:
        form = SkillForm(instance=user_skill)

    context = {
        'title': title,
        'form': form,
    }

    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    user_profile = request.user.profile
    user_skill = user_profile.skill_set.get(id=pk)
    title = "Delete Skill"

    if request.method == "POST":
        user_skill.delete()

        messages.success(request, "Skill deleted successfully.")

        return redirect("account")

    context = {
        'object': user_skill,
        'title': title,
    }

    return render(request, "delete_template.html", context)


@login_required(login_url="login")
def inbox(request):

    user_profile = request.user.profile

    user_messages = user_profile.messages.all()
    unread_count = user_messages.filter(is_read=False).count()

    context = {
        'user_messages': user_messages,
        'unread_count': unread_count,
    }

    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def view_message(request, pk):

    user_profile = request.user.profile
    user_message = user_profile.messages.get(id=pk)

    if not user_message.is_read:
        user_message.is_read = True
        user_message.save()

    context = {
        'message': user_message,
    }

    return render(request, "users/message.html", context)


@login_required(login_url="login")
def send_message(request, pk):
    developer_profile = Profile.objects.get(id=pk)
    sender_profile = request.user.profile

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.recipient = developer_profile
            new_message.sender = sender_profile
            new_message.save()

            messages.success(request, "Message sent successfully.")

            return redirect("profile", pk=developer_profile.id)

    else:
        form = MessageForm()

    context = {
        'form': form,
        'developer': developer_profile,
    }

    return render(request, "users/message_form.html", context)
