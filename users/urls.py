from django.urls import path
from users.views import sign_up, sign_in, sign_out, admin_dashboard, assign_role
from core.views import home

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    path('sign-in/', sign_in, name="sign-in"),
    path('home/', home, name="home"),
    path('sign-out/', sign_out, name="sign-out"),
    path('admin/dashboard/', admin_dashboard, name="admin-dashboard"),
    path('admin/<int:user_id>/assign-role/', assign_role, name="assign-role"),
]
