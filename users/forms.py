from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CustomRegistrationForm(forms.ModelForm):
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
        
        # Restrict from specific domains
        if email.endswith('ahmedbawanyacademy.edu.bd'):
            raise forms.ValidationError("Invalid email address")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        
        return email

    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get('confirm_password')

    #     if password and confirm_password and password != confirm_password:
    #         raise forms.ValidationError("Passwords do not match")

    #     return cleaned_data
    
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password'])
    #     if commit:
    #         user.save()
    #     return user