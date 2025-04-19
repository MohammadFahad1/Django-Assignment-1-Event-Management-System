from django.urls import path
from users.views import sign_up, sign_in
from core.views import home

urlpatterns = [
    path('sign-up/', sign_up, name="sign-up"),
    path('sign-in/', sign_in, name="sign-in"),
    path('home', home, name="home"),
]
