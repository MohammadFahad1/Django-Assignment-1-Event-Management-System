from django import forms
from events.models import *

class StyledFormMixin:
    default_classes = "border-2 border-gray-500 p-2 my-2 w-full rounded-lg shadow-sm focus:border-rose-400"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field.label.lower()}',
                    'rows': "5"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field.label.lower()}'
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
            else:
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field.label.lower()}'
                })

class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()


class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        exclude = []
    
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()


class ParticipantModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        exclude = []
        widgets = {
            'event': forms.CheckboxSelectMultiple(attrs={'class': 'border-2 border-gray-500'})
        }

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()