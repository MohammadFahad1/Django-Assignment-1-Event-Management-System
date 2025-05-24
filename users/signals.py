from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

receiver(post_save, sender=User)
def confirm_user_email(sender, instance, created, **kwargs):
    pass