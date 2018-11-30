from django.contrib import admin
from books.models import Publisher, Author, Book

# Register your models here.
admin.site.register([Publisher, Author, Book])