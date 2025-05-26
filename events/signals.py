from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.contrib.auth.models import User
from events.models import *

@receiver(post_save, sender=Event)
def rsvp_event(sender, instance, created, **kwargs):
    if created:
        assigned_emails = [participant.email for participant in instance.participants.all()]