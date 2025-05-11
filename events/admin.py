from django.contrib import admin
from events.models import Category, Event

admin.site.register(Category)
admin.site.register(Event)