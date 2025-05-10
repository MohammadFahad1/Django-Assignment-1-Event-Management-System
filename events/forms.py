from django import forms
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from events.models import *

class StyledFormMixin:
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "border-2 border-gray-500 p-2 my-2 w-full rounded-lg shadow-sm focus:border-rose-400"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                if field.label.lower() == 'date':
                    field.widget.attrs.update({
                        'class': self.default_classes,
                        'placeholder': f'YYYY-MM-DD'
                    })
                elif field.label.lower() == 'time':
                    field.widget.attrs.update({
                        'class': self.default_classes,
                        'placeholder': f'HH:MM:SS'
                    })
                else:
                    field.widget.attrs.update({
                        'class': self.default_classes,
                        'placeholder': f'Enter {field.label.lower()}'
                    })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field.label.lower()}',
                    'rows': "5"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': 'border-2 border-gray-500 p-2 mb-2 rounded-lg shadow-sm focus:border-rose-400',
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'mb-2',
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.DateField):
                field.widget.attrs.update({
                    'class': 'border-2 border-gray-500 p-2 mb-2 rounded-lg shadow-sm focus:border-rose-400',
                    'placeholder': 'YYYY-MM-DD',
                    'class': 'mb-2',
                })
            else:
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field.label}'
                })

class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']



class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        exclude = []

class ParticipantModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        exclude = []
        widgets = {
            'event': forms.CheckboxSelectMultiple(attrs={'class': 'border-2 border-gray-500'})
        }
    
@receiver(post_save, sender=Event)
def rsvp_event(sender, instance, created, **kwargs):
    if created:
        assigned_emails = [participant.email for participant in instance.participants.all()]

        # send_mail(
        #     "Subject here",
        #     "Here is the message.",
        #     "from@example.com",
        #     ["to@example.com"],
        #     fail_silently=False,
        # )