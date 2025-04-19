from django.urls import path
from users.views import sign_up, sign_in, sign_out
from core.views import home

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    path('sign-in/', sign_in, name="sign-in"),
    path('home/', home, name="home"),
    path('sign-out/', sign_out, name="sign-out"),
]
