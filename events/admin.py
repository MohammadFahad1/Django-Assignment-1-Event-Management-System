from django.contrib import admin
from events.models import Category, Event, Participant

admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Participant)