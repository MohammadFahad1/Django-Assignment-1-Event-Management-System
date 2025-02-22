from django.shortcuts import render
# from django.http import HttpResponse
from events.forms import CategoryModelForm, EventModelForm, ParticipantModelForm

def home_page(request):
    # form = CategoryModelForm()
    # form = ParticipantModelForm()
    # form = EventModelForm()
    # if request.method == 'POST':
    #     print(request.POST)
    return render(request, 'dashboard/dashboard.html')
