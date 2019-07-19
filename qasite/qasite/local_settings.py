import os

DEBUG = True

STATIC_ROOT = 'C:/Python27/untitled2/qasite/static'

MEDIA_ROOT = 'C:/Python27/untitled2/qasite/media'

ALLOWED_HOSTS = '*'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/project/qasite.s.news/data/db.sqlite3',
    }
}
