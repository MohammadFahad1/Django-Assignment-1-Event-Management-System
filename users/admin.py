from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),

        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'location', 'profile_image')}),

        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),

        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone', 'location', 'profile_image', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
admin.site.site_header = "Event Management System Admin"
admin.site.site_title = "Event Management System Admin Portal"
