from django.urls import path
from events.views import dashboard, delete_event, events, home_page, event_detail, participants, categories, update_event

urlpatterns = [
    path('', home_page),
    path('details/', event_detail),
    path('dashboard/', dashboard),
    path('events/', events, name='event-list'),
    path('update_event/<int:id>', update_event, name='update-event'),
    path('delete_event/<int:id>', delete_event, name='delete-event'),
    path('participants/', participants, name='participant-list'),
    path('participants/<int:id>', participants, name='update-participant'),
    path('participants/<int:id>', participants, name='delete-participant'),
    path('categories/', categories)
]
