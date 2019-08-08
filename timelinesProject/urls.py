from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('timelines/', include('timelinesGenerator.urls')),
    path('admin/', admin.site.urls),
]