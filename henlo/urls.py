from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from henlo_app import views

router = routers.DefaultRouter()
admin.site.site_header = 'Henlo administration'
admin.site.index_title = ''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/sync', views.sync_view),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
