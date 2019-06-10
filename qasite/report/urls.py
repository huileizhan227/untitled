from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.index, name='index'),
    path('project/<str:project_name>/', views.project, name='project'),
    path('project/<str:project_name>/<int:build_id>', views.detail, name='detail'),
    path('upload/', views.upload, name='upload'),
]
