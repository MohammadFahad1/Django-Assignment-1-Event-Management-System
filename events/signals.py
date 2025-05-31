from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.core.mail import send_mail
from django.contrib.auth.models import User
from events.models import RSVP
    
@receiver(m2m_changed, sender=RSVP)
def rsvp_event(sender, instance, created, **kwargs):
    if created:
        print(instance.__dict__)
        # event = instance.event
        # user = instance.user
        # host_email = get_user_email(user)
        # send_mail('RSVP Confirmation', f'You have RSVPed to {event.title}.', host_email, [host_email])
