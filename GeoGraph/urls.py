from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('core.api.urls')),
    path('api/v2/', include('geodetics.urls')),
]
