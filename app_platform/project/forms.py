from pyexpat import model
from .models import Project
from django import forms
from .services.docker import verify_if_docker_image_exists


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'app_image']

    # validate if the docker image as specified in the form exists
    def clean_app_image(self):
        app_image = self.cleaned_data['app_image']
        is_exists = verify_if_docker_image_exists(app_image)
        if not is_exists:
            raise forms.ValidationError(f'Docker image {app_image} does not exist')
        return app_image

