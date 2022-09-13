from django.shortcuts import render, redirect
from . import models, forms
from .services.docker import get_app_config_spec
from django.conf import settings
import json
import django.forms as django_forms


def index(request):
    """
    Show a list of all projects.
    """
    projects = models.Project.objects.all()

    context = {
        'projects': projects,
    }
    return render(request, 'project/index.html', context)



def update(request, project_slug):
    """
    Update a project.
    """
    project = models.Project.objects.get(slug=project_slug)
    if request.method == 'POST':
        form = forms.ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project:index')

    else:
        form = forms.ProjectForm(instance=project)

    return render(request, 'project/update.html', {'form': form})



def delete(request, project_slug):
    """
    Delete a project.
    """
    pass
   

def create(request):
    """
    Create a new project.
    """
    if request.method == 'POST':
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project:index')
    else:
        form = forms.ProjectForm()

    context = {
        'form': form,
    }

    return render(request, 'project/create.html', context)


def input_data(request, project_slug):
    """
    Show the input data for a project.
    """
    project = models.Project.objects.get(slug=project_slug)

    base_url = settings.NOCODB_URL
    nocodb_url = f"{base_url.rstrip('/')}/dashboard/#/nc/{project.noco_project_id}/auth"

    context = {
        "noco_url": nocodb_url,
        "project": project,
    }

    return render(request, 'project/data.html', context)


def list_jobs(request, project_slug):
    """
    List all jobs for a project.
    """
    project = models.Project.objects.get(slug=project_slug)
    jobs = project.job_set.all()

    context = {
        "project": project,
        "jobs": jobs
    }

    return render(request, 'project/list_jobs.html', context)


def create_job(request, project_slug):
    """
    Create a run for a project.
    """
    project = models.Project.objects.get(slug=project_slug)

    # get the config spec of the app_image
    config_spec = get_app_config_spec(project.app_image)
    config = json.loads(config_spec)

    # create a dynamic form based on the json schema as specified in config
    json_schema_type_to_field_type = {
        "string": django_forms.CharField,
        "integer": django_forms.IntegerField,
        "number": django_forms.FloatField,
        "boolean": django_forms.BooleanField,
    }

    class DynamicJobForm(django_forms.Form):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in config['properties']:
                field_type = json_schema_type_to_field_type[config['properties'][field]['type']]
                self.fields[field] = field_type(
                    label=field
                )


    if request.method == 'POST':
        form = DynamicJobForm(request.POST)
        if form.is_valid():
            # convert form data to json
            config = json.dumps(form.cleaned_data)
            # create a new job
            job = models.Job(
                project=project,
                config=config
            )
            job.save()

            # kickoff the container run job
            job.start_run()
            return redirect('project:list_jobs', project_slug=project_slug)

    else:
        form = DynamicJobForm()

    return render(request, 'project/create_job.html', {'form': form, 'project': project})


def job_logs(request, project_slug, job_id):
    """
    Show the logs for a job.
    """

    job = models.Job.objects.get(id=job_id)

    context = {
        "job": job,
        "project_slug": project_slug,
    }

    return render(request, 'project/job_logs.html', context)