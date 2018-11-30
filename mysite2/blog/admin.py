from django.contrib import admin
from blog.models import BlogPost

# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'timestamp')
    search_fields = ('title', 'body')

admin.site.register(BlogPost,BlogPostAdmin)