from django.urls import path
from users.views import activate_user, create_group, sign_up, sign_in, sign_out, admin_dashboard, assign_role, group_list
from core.views import no_access

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    path('sign-in/', sign_in, name="sign-in"),
    path('no-access/', no_access, name="no-access"),
    path('sign-out/', sign_out, name="sign-out"),
    path('admin/dashboard/', admin_dashboard, name="admin-dashboard"),
    path('admin/<int:user_id>/assign-role/', assign_role, name="assign-role"),
    path('admin/create-group/', create_group, name="create-group"),
    path('admin/group-list/', group_list, name='group_list'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name="activate-user"),
]
