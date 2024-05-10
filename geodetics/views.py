import json

import imageio
from geomag import geomag
from geographiclib.geodesic import Geodesic
from math import atan2, degrees, radians, sin, cos, tan

from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['POST'])
def calc_anomaly(request):
    request_data = json.loads(request.body)
    lat = float(request_data["lat"])
    lon = float(request_data["lon"])

    if lat == 0:
        # Log error (use Django's logging methods)
        return JsonResponse({
            "lat": lat,
            "lon": lon,
            "anomaly": 0
        })
    elif lon == 0:
        # Log error (use Django's logging methods)
        return JsonResponse({
            "lat": lat,
            "lon": lon,
            "anomaly": 0
        })

    file_path = "EGM96 - 5'.pgm"
    image = imageio.imread(file_path)

    height, width = image.shape

    geod = Geodesic.WGS84
    g = geod.Direct(lat, lon, 0, 1000)
    x = (g['lon2'] + 180) * (width - 1) / 360
    y = (90 - g['lat2']) * (height - 1) / 180

    elevation = image[int(y), int(x)]
    elevation_str = str(elevation)

    return JsonResponse({
        "lat": lat,
        "lon": lon,
        "anomaly": elevation_str
    })


@api_view(['POST'])
def get_data(request):
    request_data = json.loads(request.body)
    target_coords = request_data["target_coords"]
    origin_coords = request_data["origin_coords"]

    if target_coords is None:
        # Log error (use Django's logging methods)
        return JsonResponse({
            "tangage": 0,
        })

    if origin_coords is None:
        # Log error (use Django's logging methods)
        return JsonResponse({
            "tangage": 0,
        })

    diff_longitude = radians(target_coords[1] - origin_coords[1])

    y = sin(diff_longitude)
    x = cos(radians(target_coords[0])) * tan(radians(origin_coords[0])) - sin(radians(target_coords[0])) * cos(
        diff_longitude)
    tangage = degrees(atan2(y, x))

    return JsonResponse({
        "tangage": tangage,
    })


@api_view(['POST', 'OPTIONS'])
def get_magnetic_declination(request):
    request_data = json.loads(request.body)
    lat = float(request_data["lat"])
    lon = float(request_data["lon"])

    mag = geomag.GeoMag()
    result = mag.GeoMag(lat, lon)
    declination = result.dec

    return JsonResponse({
        "lat": lat,
        "lon": lon,
        "magnetic_declination": declination
    })
