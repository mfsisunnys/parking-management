from django.urls import path

from .views import get_slot_detail

urlpatterns = [
    path('', get_slot_detail, name='get_slot_detail')
]