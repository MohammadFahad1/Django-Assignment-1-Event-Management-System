from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def sign_up(request):
    form = UserCreationForm() # Default form provided by Django
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # Default form provided by Django
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('sign-up')
        
    return render(request, 'registration/register.html', {"form": form})