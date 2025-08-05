from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def no_access(request):
    return render(request, 'no_access.html')