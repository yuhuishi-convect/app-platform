from django.urls import path

from . import views

app_name = 'project'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<str:project_slug>/', views.update, name='update'),
    path('<str:project_slug>/data/', views.input_data, name='data'),
    path('<str:project_slug>/delete/', views.delete, name='delete'),
    path('<str:project_slug>/jobs', views.list_jobs, name='list_jobs'),
    path('<str:project_slug>/job/create', views.create_job, name='create_job'),
    path('<str:project_slug>/job/<int:job_id>/logs', views.job_logs, name='job_logs'),
]