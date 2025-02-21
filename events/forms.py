from django import forms
from events.models import *

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = []