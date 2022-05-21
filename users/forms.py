from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2", ]

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "input"})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input input--text'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ["owner"]

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "input input--text"})


class MessageForm(ModelForm):

    class Meta:
        model = Message
        exclude = ["sender", "recipient", "is_read"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})

