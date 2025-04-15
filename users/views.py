from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User

from users.forms import CustomRegistrationForm, RegisterForm

# Create your views here.
def sign_up(request):
    form = CustomRegistrationForm() # Default form provided by Django
    
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST) # Default form provided by Django
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
        #     username = form.cleaned_data('username')
        #     password = form.cleaned_data('password1')
        #     confirm_password = form.cleaned_data('password2')

        #     if password and confirm_password and password == confirm_password:
        #         User.objects.create(username=username, password=password)
        #         messages(request, 'User created successfully')
        #     else:
        #         messages.error(request, 'Password does not match')
        # else:
        #     messages.message(request, 'Error creating user')
        
    return render(request, 'registration/register.html', {"form": form})