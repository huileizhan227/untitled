from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from blog.models import BlogPost

def blog_index(request):
    bloglist = BlogPost.objects.all()
    blog_list = {'blog_list':bloglist}
    return render(request, 'index.html', blog_list)
