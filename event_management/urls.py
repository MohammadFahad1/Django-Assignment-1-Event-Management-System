from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from events.views import home_page, event_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('details/', event_detail)
] + debug_toolbar_urls()
