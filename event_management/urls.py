from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from events.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page)
] + debug_toolbar_urls()
