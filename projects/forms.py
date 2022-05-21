from django.forms import ModelForm
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ["title", "featured_image", "description", "demo_link", "source_link", "tags"]

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input input--text'})


class ReviewForm(ModelForm):

    class Meta:
        model = Review
        fields = ["value", "body"]

        labels = {
            'value': "Place your vote",
            'body': "Add a comment with your vote",
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})
