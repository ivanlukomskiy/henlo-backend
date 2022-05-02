from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from henlo_app import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', admin.site.urls),
    path('api/v1/sync', views.sync),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
