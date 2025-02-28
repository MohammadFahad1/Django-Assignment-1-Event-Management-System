from math import e
from django.shortcuts import redirect, render
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
                return redirect('event-list')
                
        context = {"form": event_form}
        return render(request, 'event_form.html', context)
    
    events = Event.objects.select_related('category').prefetch_related('participants').all().order_by('date')
    context = {"events": events}
    return render(request, 'dashboard/events_table.html', context)

def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event updated successfully")
            return redirect('event-list')

    return render(request, 'event_form.html', {"form": event_form})

def delete_event(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    messages.success(request, 'Event deleted successfully')
    return redirect('event-list')

def participants(request):
    participant_form = ParticipantModelForm()
    action = request.GET.get('action', 'all')

    if action == 'add':
        if request.method == 'POST':
            part_form = ParticipantModelForm(request.POST)

            if part_form.is_valid():
                part_form.save()
                messages.success(request, 'Participant added successfully')
                return redirect('participant-list')
            else:
                messages.error(request, 'Error adding participant')
                return render(request, 'participant_form.html', {"form": part_form})
            
        return render(request, 'participant_form.html', {"form": participant_form})

    participants = Participant.objects.prefetch_related('event').all()
    return render(request, 'dashboard/participants_table.html', {"participants": participants})

def categories(request):
    category_form = CategoryModelForm()

    context = {"form": category_form}
    return render(request, 'category_form.html', context)