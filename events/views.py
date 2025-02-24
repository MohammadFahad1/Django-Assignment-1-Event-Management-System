from django.shortcuts import render
# from django.http import HttpResponse
from events.forms import CategoryModelForm, EventModelForm, ParticipantModelForm

def home_page(request):
    return render(request, 'home_page.html')

def event_detail(request):
    return render(request, 'event_detail.html')