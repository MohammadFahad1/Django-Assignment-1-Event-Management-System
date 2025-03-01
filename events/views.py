from math import e
from django.shortcuts import redirect, render
# from django.http import HttpResponse
from events.forms import CategoryModelForm, EventModelForm, ParticipantModelForm
from django.contrib import messages
from events.models import *
from django.utils.timezone import now
from django.db.models import Count, Q

def home_page(request):
    events = Event.objects.select_related('category').prefetch_related('participants').annotate(participants_count=Count('participants')).order_by('date')
    return render(request, 'home_page.html', {"events": events})

def event_detail(request, id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
    return render(request, 'event_detail.html', {"event": event})

def dashboard(request):
    type = request.GET.get('type', 'all')
    today = now().date()

    counts = Event.objects.aggregate(
        total_participant=Count('participants', distinct=True),
        total_events=Count('id', distinct=True),
        upcomming_events=Count('id', filter=Q(date__gte= today), distinct=True),
        past_events=Count('id', filter=Q(date__lt= today), distinct=True)
    )

    # Retrieve event data
    if type == 'upcomming':
        events = Event.objects.filter(date__gte=today).annotate(participants_count=Count('participants')).order_by('date')
    elif type == 'past':
        events = Event.objects.filter(date__lt=today).annotate(participants_count=Count('participants')).order_by('-date')
    else:
        events = Event.objects.annotate(participants_count=Count('participants')).order_by('date')

    context = {
        "counts": counts,
        "events": events
    }

    return render(request, 'dashboard/dashboard_home.html', context)

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

    participants = Participant.objects.prefetch_related('event').all().order_by('id')
    return render(request, 'dashboard/participants_table.html', {"participants": participants})

def update_participant(request, id):
    participant = Participant.objects.get(id=id)
    participant_form = ParticipantModelForm(instance=participant)

    if request.method == 'POST':
        participant_form = ParticipantModelForm(request.POST, instance=participant)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, 'Participant updated successfully')
            return redirect('participant-list')
        else:
            messages.error(request, "Error updating participant")
    
    return render(request, 'participant_form.html', {"form": participant_form})

def delete_participant(request, id):
    participant = Participant.objects.get(id=id)
    participant.delete()
    messages.success(request, 'Participant deleted successfully')
    return redirect('participant-list')

def categories(request):
    category_form = CategoryModelForm()
    action = request.GET.get('action', 'all')
    if action == 'add':
        if request.method == 'POST':
            category_form = CategoryModelForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                messages.success(request, 'Category added successfully')
                return redirect("category-list")
        return render(request, 'category_form.html', {"form": category_form})
    
    categories = Category.objects.all().order_by('id')
    context = {"categories": categories}
    return render(request, 'dashboard/category_table.html', context)

def update_category(request, id):
    category = Category.objects.get(id=id)
    category_form = CategoryModelForm(instance=category)
    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST, instance=category)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Category updated successfully")
            return redirect('category-list')
        else:
            messages.error('Something went wrong while updating category')

    return render(request, 'category_form.html', {"form": category_form})

def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('category-list')