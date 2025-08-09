from django.shortcuts import render


def no_access(request):
    return render(request, 'no_access.html')