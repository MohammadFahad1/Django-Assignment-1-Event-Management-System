from django.urls import path
from users.views import activate_user, create_group, sign_up, SignInView, sign_out, user_list, assign_role, group_list, delete_group, ProfileView
from core.views import no_access

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    path('sign-in/', SignInView.as_view(), name="sign-in"),
    path('no-access/', no_access, name="no-access"),
    path('sign-out/', sign_out, name="sign-out"),
    path('admin/dashboard/user-list/', user_list, name="user-list"),
    path('admin/<int:user_id>/assign-role/', assign_role, name="assign-role"),
    path('admin/create-group/', create_group, name="create-group"),
    path('admin/group-list/', group_list, name='group_list'),
    path('admin/group/<int:group_id>/delete/', delete_group, name='delete-group'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name="activate-user"),
    path('profile/', ProfileView.as_view(), name="activate-user"),
]
