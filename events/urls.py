from django.urls import path
from events.views import dashboard, delete_event, delete_participant, events, home_page, event_detail, participants, categories, update_event, update_participant

urlpatterns = [
    path('', home_page),
    path('details/', event_detail),
    path('dashboard/', dashboard),
    path('events/', events, name='event-list'),
    path('update_event/<int:id>', update_event, name='update-event'),
    path('delete_event/<int:id>', delete_event, name='delete-event'),
    path('participants/', participants, name='participant-list'),
    path('update_participant/<int:id>', update_participant, name='update-participant'),
    path('delete_participant/<int:id>', delete_participant, name='delete-participant'),
    path('categories/', categories)
]
