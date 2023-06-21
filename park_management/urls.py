from django.urls import path

from .views import parkingLot, park, unpark


urlpatterns = [
    path('vehicle/park/', park, name='park'),
    path('parking-lot/', parkingLot, name='parkingLot'),
    path('vehicle/unpark/', unpark, name='unpark'),
]