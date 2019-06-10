from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'ued'

urlpatterns = [
    path('', views.index, name='index'),
    path('doc/<str:platform_name>/', views.platform, name='platform'),
    path('doc/<str:platform_name>/<str:version>', views.detail, name='detail'),
    path('api/upload/', views.upload, name='upload'),
    path('api/reset/', views.reset, name='reset')
]
