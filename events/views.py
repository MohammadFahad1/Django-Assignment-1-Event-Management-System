from math import e
from django.shortcuts import redirect, render
from events.forms import CategoryModelForm, EventModelForm, ParticipantModelForm
from django.contrib import messages
from events.models import *
from django.utils.timezone import now
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from users.views import is_admin
from django.views.generic import ListView
from django.views import View
from django.utils.decorators import method_decorator

# Test for users
def is_admin_or_organizer(user):
    return user.groups.filter(name__in=['Admin', 'Organizer']).exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()

# Home page view
def home_page(request):
    search = request.GET.get('search', '')
    today = now().date()
    if search:
        events = Event.objects.filter(Q(name__icontains=search) | Q(location__icontains=search)).select_related('category').prefetch_related('participants').annotate(participants_count=Count('participants')).order_by('date')
        return render(request, 'home_page.html', {"events": events, "search": True, "search_txt": search, "today": today})
        

    events = Event.objects.select_related('category').prefetch_related('participants').annotate(participants_count=Count('participants')).order_by('date')
    return render(request, 'home_page.html', {"events": events, "today": today})

# Event detail view
def event_detail(request, id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
    return render(request, 'event_detail.html', {"event": event})

# Organizer dashboard view
@login_required
@user_passes_test(is_admin_or_organizer, login_url='no-access')
def organizer_dashboard(request):
    type = request.GET.get('type', 'todays')
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
    elif type == 'all':
        events = Event.objects.annotate(participants_count=Count('participants')).order_by('date')
    else:
        events = Event.objects.filter(date=today).annotate(participants_count=Count('participants')).order_by('date')

    context = {
        "counts": counts,
        "events": events,
        "type": type
    }

    return render(request, 'dashboard/dashboard_home.html', context)

@login_required
@permission_required('events.add_event', raise_exception=False, login_url='no-access')
def events(request):
    event_form = EventModelForm()
    action = request.GET.get('action', 'all')
    if action == 'add':
        if request.method == 'POST':
            event_form = EventModelForm(request.POST, request.FILES)
            if event_form.is_valid():
                event_form.save()
                messages.success(request, 'Event added successfully')
                return redirect('event-list')
                
        context = {"form": event_form}
        return render(request, 'event_form.html', context)
    
    events = Event.objects.select_related('category').prefetch_related('participants').all().order_by('date')
    context = {"events": events}
    return render(request, 'dashboard/events_table.html', context)

@login_required
@permission_required('events.change_event', raise_exception=False, login_url='no-access')
def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event, files=request.FILES)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event updated successfully")
            return redirect('event-list')

    return render(request, 'event_form.html', {"form": event_form})

@login_required
@permission_required('events.delete_event', raise_exception=False, login_url='no-access')
def delete_event(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    messages.success(request, 'Event deleted successfully')
    return redirect('event-list')

@login_required
@user_passes_test(is_admin, login_url='no-access')
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

    participants = User.objects.all().prefetch_related('participants').order_by('id')
    return render(request, 'dashboard/participants_table.html', {"participants": participants})

@login_required
@user_passes_test(is_admin, login_url='no-access')
def update_participant(request, id):
    participant = User.objects.get(id=id)
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

@login_required
@user_passes_test(is_admin, login_url='no-access')
def delete_participant(request, id):
    participant = User.objects.get(id=id)
    participant.delete()
    messages.success(request, 'Participant deleted successfully')
    return redirect('participant-list')

@login_required
@permission_required('events.view_category', raise_exception=False, login_url='no-access')
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
    
    categories = Category.objects.prefetch_related('event_category').all().order_by('id')
    context = {"categories": categories}
    return render(request, 'dashboard/category_table.html', context)

@login_required
@permission_required('events.change_category', raise_exception=False, login_url='no-access')
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

@login_required
@permission_required('events.delete_category', raise_exception=False, login_url='no-access')
def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, 'Category deleted successfully')
    return redirect('category-list')

# RSVP using class based view
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_participant, login_url='no-access'), name='dispatch')
@method_decorator(permission_required('events.add_rsvp', raise_exception=False, login_url='no-access'), name='dispatch')
class RSVPView(View):
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        user = request.user

        if RSVP.objects.filter(event=event, user=user).exists():
            messages.error(request, 'You have already RSVPed to this event')
        else:
            rsvp_instance = RSVP.objects.create(lastUserRSVPed=user, lastEventRSVPed=event)
            event.rsvps.add(rsvp_instance)
            user.rsvps.add(rsvp_instance)
            rsvp_instance.save()

            event.participants.add(user)
            messages.success(request, 'You have RSVPed to this event')

        return redirect('home_page')
    

# RSVP List using Class based view
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_participant, login_url='no-access'), name='dispatch')
class RSVPListView(ListView):
    model = Event
    template_name = 'dashboard/rsvp_table.html'
    context_object_name = 'events'

    def get_queryset(self):
        user = self.request.user
        return user.participants.all()

@login_required
def dashboard(request):
    if is_admin_or_organizer(request.user):
        return redirect('main-dashboard')
    elif is_participant(request.user):
        return redirect('rsvp-list')
    else:
        return redirect('no-access')