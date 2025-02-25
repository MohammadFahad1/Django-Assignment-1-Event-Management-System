from django.urls import path
from events.views import dashboard, events, home_page, event_detail

urlpatterns = [
    path('', home_page),
    path('details/', event_detail),
    path('dashboard/', dashboard),
    path('events', events)
]
