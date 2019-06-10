import os

DEBUG = True

STATIC_ROOT = '/home/project/qasite.s.news/static'

MEDIA_ROOT = '/home/project/qasite.s.news/media'

ALLOWED_HOSTS = '*'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/project/qasite.s.news/data/db.sqlite3',
    }
}
