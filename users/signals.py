from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import models

from .models import Profile
from .utils import send_email_message


@receiver(post_save, sender=models.User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name + " " + user.last_name,
        )

        subject = "Welcome to DevSearch!"
        message = "We're glad you're here."

        send_email_message(subject=subject, message=message, recipients=[profile.email])
    else:
        pass


@receiver(post_save, sender='users.Profile')
def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    names = profile.name.split()

    if not created and len(names) > 1:
        user.first_name = names[0]
        user.last_name = names[1]
        user.email = profile.email
        user.username = profile.username

        user.save()
    elif not created:
        user.first_name = names[0]
        user.email = profile.email
        user.username = profile.username

        user.save()


@receiver(post_delete, sender='users.Profile')
def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()

    print("Deleting user")
