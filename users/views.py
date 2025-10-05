from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from users.forms import CreateGroupForm, CustomRegistrationForm, AssignRoleForm, LoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

# Test for users
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

# Create your views here.
def sign_up(request):
    form = CustomRegistrationForm() # Default form provided by Django
    
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST) # Default form provided by Django
        if form.is_valid():
            form.save()
            # user = form.save(commit=False)
            # user.is_active = False
            # user.save()
            messages.success(request, 'A confirmation email has been sent to your email address. Please confirm your email address to activate your account.')
            return redirect('sign-in')
        
    return render(request, 'registration/register.html', {"form": form})

class SignInView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        return next_url if next_url else super().get_success_url()

@login_required
def sign_out(request):
    if request.method == 'POST':
        messages.success(request, 'Logged out successfully')
        logout(request)
        return redirect('sign-in')

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)

        if user.is_active == False:
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Your account has been activated. You can now log in.')
                return redirect('sign-in')
        else:
            messages.error(request, 'Your account is already activated. You can now log in.')
            return redirect('sign-in')

    except User.DoesNotExist:
        messages.error(request, 'Invalid activation link')
        return redirect('sign-in')

@login_required
@user_passes_test(is_admin, login_url='no-access')
def user_list(request):
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {"users": users})

@login_required
@user_passes_test(is_admin, login_url='no-access')
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
            return redirect('user-list')

    return render(request, 'admin/assign_role.html', {"form": form})

@login_required
@user_passes_test(is_admin, login_url='no-access')
def create_group(request):
    form = CreateGroupForm()

    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f'Group {group.name} has been created successfully')
            return redirect('create-group')
    
    return render(request, 'admin/create_group.html', {"form": form})

@login_required
@user_passes_test(is_admin, login_url='no-access')
def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.delete()
    messages.success(request, f'Group {group.name} has been deleted successfully')
    return redirect('group_list')

@login_required
@user_passes_test(is_admin, login_url='no-access')
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'admin/group_list.html', {"groups": groups})

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()
        context['group'] = user.groups.first().name if user.groups.exists() else 'No Role Assigned'
        context['is_active'] = user.is_active
        context['member_since'] = user.date_joined.strftime('%B %d, %Y')
        context['last_login'] = user.last_login.strftime('%B %d, %Y, %I:%M %p') if user.last_login else 'First time login'
        context['is_staff'] = user.is_staff
        context['is_superuser'] = user.is_superuser
        
        return context