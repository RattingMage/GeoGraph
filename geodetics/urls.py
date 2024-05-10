from django.urls import path
from .views import calc_anomaly, get_data, get_magnetic_declination
urlpatterns = [
    path('calc_anomaly/', calc_anomaly, name='calc_anomaly'),
    path('get_data/', get_data, name='get_data'),
    path('get_magnetic_declination/', get_magnetic_declination, name='get_magnetic_declination'),
]
