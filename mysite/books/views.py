from django.shortcuts import render
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from books.models import Book
from books.forms import ContactForm
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect

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
@csrf_protect
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # cd = form.cleaned_data
            # send_mail(
            #     cd['subject'],
            #     cd['message'],
            #     cd.get('email', 'noreply@example.com'),
            #     ['siteowner@example.com'],
            # )
            return HttpResponseRedirect('/contact/thanks')
    else:
        form = ContactForm(
            initial={'subject':'I love your site!'} #为字subject段添加初始值
        )
    return render(request, 'contact_form.html', {'form':form})

def contact_thanks(request):
    return render(request,'contact_thanks.html')



