from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from django.conf import settings

import main

# each apps
from main.urls import apiurls as main_urls

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += main_urls


if settings.DEBUG == False:
  urlpatterns.extend([
    url(r'', main.views.logout),
  ])
