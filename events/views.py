from django.shortcuts import render
# from django.http import HttpResponse
from events.forms import CategoryModelForm, EventModelForm, ParticipantModelForm
from django.contrib import messages
from events.models import *

def home_page(request):
    return render(request, 'home_page.html')

def event_detail(request):
    return render(request, 'event_detail.html')

def dashboard(request):
    return render(request, 'dashboard/dashboard_home.html')

def events(request):
    event_form = EventModelForm()
    action = request.GET.get('action', 'all')
    if action == 'add':
        if request.method == 'POST':
            event_form = EventModelForm(request.POST)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, 'Event added successfully')
                return render(request, 'dashboard/events_table.html')
                
        context = {"form": event_form}
        return render(request, 'event_form.html', context)
    elif action == 'edit':
        event_form = EventModelForm()
    
    events = Event.objects.all()
    context = {"events": events}
    return render(request, 'dashboard/events_table.html', context)

def participants(request):
    participant_form = ParticipantModelForm()

    context = {"form": participant_form}
    return render(request, 'participant_form.html', context)

def categories(request):
    category_form = CategoryModelForm()

    context = {"form": category_form}
    return render(request, 'category_form.html', context)