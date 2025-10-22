from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        # Assign a default role to the user
        participant_group, created = Group.objects.get_or_create(name='Participant')
        instance.groups.clear()
        instance.groups.add(participant_group)

        # Generate activation token
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"

        subject = 'Activate your account'
        message = f"Hi {instance.username}, \n\nPlease activate your account by clicking the link below: \n\n{activation_url}\n\nIf you did not create this account, you can ignore this email.\n\nBest regards,\nEvent Management System\n\n\nThank You"
        recipient_list = [instance.email]

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Failed to send mail to {instance.email}: {str(e)}")
