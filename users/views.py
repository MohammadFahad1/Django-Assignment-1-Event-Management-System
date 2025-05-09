from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegistrationForm, AssignRoleForm

# Create your views here.
def sign_up(request):
    form = CustomRegistrationForm() # Default form provided by Django
    
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST) # Default form provided by Django
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
        
    return render(request, 'registration/register.html', {"form": form})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return redirect('sign-in')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/login.html')

def sign_out(request):
    if request.method == 'POST':
        messages.success(request, 'Logged out successfully')
        logout(request)
        return redirect('sign-in')
    
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {"users": users})

def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.groups.clear()
            user.groups.add(role)
            user.save()
            messages.success(request, f'User {user.username} has been assigned to the {role.name} role')
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})