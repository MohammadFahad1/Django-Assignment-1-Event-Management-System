from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.contrib.auth.models import User
from events.models import RSVP, Event
from django.conf import settings
    
@receiver(post_save, sender=RSVP)
def rsvp_event(sender, instance, created, **kwargs):
       if created:
            user = User.objects.get(id=instance.lastUserRSVPed_id)
            event = Event.objects.get(id=instance.lastEventRSVPed_id)
            recipient_list = [user.email]
            print(recipient_list)
            subject = f'RSVP Confirmation for {event.name}'
            message = f"""
            Dear {user.first_name},

            We are pleased to inform you that your RSVP for the event '{event.name}' has been successfully recorded.

            The event details are as follows:
            Title: {event.name}
            Date: {event.date}
            Time: {event.time}
            Location: {event.location}

            If you have any questions or need further information, please do not hesitate to contact us at {settings.EMAIL_HOST_USER}.

            Thank you for your interest in our event!

            Best regards,
            The Events Team
            """
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
