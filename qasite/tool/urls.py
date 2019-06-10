from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'tool'

urlpatterns = [
    path('', views.index, name='index'),
    path('checkurl/', views.check_url, name='check_url'),
    path('checkurl-report/', views.check_url_report, name='check_url_report'),
    path('api/do-check-url/', views.do_check_url, name='do_check_url'),
    path('api/check-url-percent/', views.check_url_percent, name='check_url_percent'),
]
