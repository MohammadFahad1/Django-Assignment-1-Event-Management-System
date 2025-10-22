from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='event_thumbnails/', blank=True, null=True, default='event_thumbnails/default_thumbnail.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="event_category", default=1)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="participants")

    def __str__(self):
        return f"{self.name} - {self.date} - {self.time}"

class RSVP(models.Model):
    lastUserRSVPed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    lastEventRSVPed = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    event = models.ManyToManyField(Event, related_name="rsvps", blank=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="rsvps", blank=True)
    Timestamp = models.DateTimeField(auto_now_add=True)