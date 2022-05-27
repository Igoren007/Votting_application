from django.contrib import admin
from django.urls import path, include
from poll_app.views import *
from poll_app import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls)),
]
