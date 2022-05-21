from smtplib import SMTPException, SMTPAuthenticationError

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile, Skill


def search_profiles(request):
    search_query = ""
    profile_list = None

    if request.GET.get('search_field'):
        search_query = request.GET.get('search_field')

        skill_list = Skill.objects.filter(
            Q(name__icontains=search_query)
        )
        profile_list = Profile.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(skill__in=skill_list)
        )
    else:
        profile_list = Profile.objects.all()

    return profile_list, search_query


def paginate_profiles(request, profiles):
    results = 3
    page = 1
    profiles = list(profiles)
    paginator = Paginator(profiles, results)

    try:
        page = request.GET.get("page", page)
        profile_list = paginator.page(page)

    except EmptyPage:
        messages.error(request, "That page has no results")
        page = 1
        profile_list = paginator.page(page)

    except PageNotAnInteger:
        messages.error(request, "That page is invalid")
        page = 1
        profile_list = paginator.page(page)

    left_index = int(page) - 4

    if left_index < 1:
        left_index = 1

    right_index = int(page) + 5

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index)

    return profile_list, custom_range


def send_email_message(subject, message, recipients):
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipients, fail_silently=False)

    except SMTPException:
        print("An error occurred")

    except SMTPAuthenticationError:
        print("The username and password were not accepted.")
