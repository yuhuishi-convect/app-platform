# Generated by Django 3.2.4 on 2022-09-12 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='noco_project_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
