from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission, Group
from django.core.validators import validate_email
from events.forms import StyledFormMixin

class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        errors = []

        if password and confirm_password and password != confirm_password:
            errors.append("Passwords do not match")
        
        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        errors = []

        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        if errors:
            raise forms.ValidationError(errors)
        
        return password
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if validate_email(email):
            raise forms.ValidationError("Invalid email address")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name:
            raise forms.ValidationError("First name is required")
        
        if not re.match(r'^[a-zA-Z\s\.]+$', first_name):
            raise forms.ValidationError("First name must contain only letters")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name:
            raise forms.ValidationError("Last name is required")

        if not re.match(r'^[a-zA-Z\s\.]+$', last_name):
            raise forms.ValidationError("Last name must contain only letters")
        
        return last_name
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Select a role")
