from django.urls import path
from events.views import organizer_dashboard, DeleteCategoryView, delete_event, delete_participant, events, home_page, event_detail, participants, categories, RSVPView, update_category, update_event, update_participant, RSVPListView, dashboard

urlpatterns = [
    path('', home_page, name='home_page'),
    path('details/<int:id>', event_detail, name='event-detail'),
    path('main-dashboard/', organizer_dashboard, name='main-dashboard'),
    path('events/', events, name='event-list'),
    path('update_event/<int:id>', update_event, name='update-event'),
    path('delete_event/<int:id>', delete_event, name='delete-event'),
    path('participants/', participants, name='participant-list'),
    path('update_participant/<int:id>', update_participant, name='update-participant'),
    path('delete_participant/<int:id>', delete_participant, name='delete-participant'),
    path('categories/', categories, name="category-list"),
    path('update_category/<int:id>', update_category, name="update-category"),
    path('delete_category/<int:id>', DeleteCategoryView.as_view(), name="delete-category"),
    path('rsvp/<int:event_id>', RSVPView.as_view(), name="rsvp"),
    path('rsvp/list', RSVPListView.as_view(), name="rsvp-list"),
    path('dashboard/', dashboard, name='dashboard'),
]
