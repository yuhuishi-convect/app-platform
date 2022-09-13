from multiprocessing import Process
from django.db import models
from django.conf import settings
import os.path
from django.utils.text import slugify
from .services.docker import run_app_image, setup_temp_db
from .services.nocodb import setup_nocodb_project
import psutil

class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # temporary db path used by the project
    db_path = models.CharField(max_length=1024)
    # docker image name of the app 
    app_image = models.CharField(max_length=1024)

    noco_project_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    # override the save method to create a temporary db for the project
    def save(self, *args, **kwargs):
        # create the slug field from the name
        self.slug = slugify(self.name)
        # create a temporary db for the project
        if not self.db_path:
            self.db_path = os.path.join(settings.TEMP_DIR, f'{self.slug}.db')
            setup_temp_db(self.db_path, self.app_image)

        if not self.noco_project_id:
            self.noco_project_id = setup_nocodb_project(self.db_path, self.name)

        super().save(*args, **kwargs)



class Job(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # json string of the configuration
    config = models.TextField()

    # the path to the running logs
    log_path = models.CharField(max_length=1024)


    def __str__(self):
        return f"{self.project.name} - {self.created_at}"

    # override the save method to start a fire-and-foreget process to run the app
    def save(self, *args, **kwargs):
        # create a log file for the job
        if not self.log_path:
            filename = f'{self.project.slug}_{self.created_at}.log'
            filename = slugify(filename)
            self.log_path = os.path.join(settings.TEMP_DIR, filename)
        super().save(*args, **kwargs)

    def start_run(self):
        """
        Start to run the app image
        """
        config_file_name = f'{self.project.slug}_{self.created_at}.json'
        config_file_name = slugify(config_file_name)
        config_path = os.path.join(settings.TEMP_DIR, config_file_name)
        # write the config to config_path
        with open(config_path, 'w') as f:
            f.write(self.config)
        logs = run_app_image(self.project.app_image, self.project.db_path, config_path, self.log_path)
        return logs



    # return the logs of the job
    @property
    def logs(self):
        with open(self.log_path, 'r') as f:
            return f.read()