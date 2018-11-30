from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from books.models import Book

def search_form(request):
    return render(request, 'search_form2.html')

def search(request):
    if 'q' in request.GET and request.GET['q']!="":
        q = request.GET['q']
        books = Book.objects.filter(title__icontains=q)
        ctx = {}
        ctx['books'] = books
        ctx['query'] = q
        return render(request, 'search_results.html',ctx)
    else:
        return render(request, 'search_form2.html',{'error':True})
