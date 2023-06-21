from django.core.cache import cache
from django.core.serializers import deserialize

from decouple import config
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Create your views here.

total_slots = config("TOTAL_SLOTS")


def check_existing_vehicle(vehicle_number):
    """
    This function checks if the vehicle is already parked in the parking lot
    """
    totalSlots = cache.get("Slot")
    if totalSlots is None:
        return False
    else:
        totalSlots = json.loads(totalSlots)
        for slot in totalSlots:
            if slot["vehicle_number"] == vehicle_number:
                return True, slot["id"]
        return False, None


@throttle_classes([AnonRateThrottle])
@api_view(["GET"])
def get_slot_detail(request):
    """
    This function returns the slot details for a given slot id
    """
    try:
        slot_id = request.GET.get("slot_id")

        if slot_id is None or slot_id == "":
            return Response(
                {"message": "Please provide slot id", "details": None},
                status=status.HTTP_400_BAD_REQUEST,
            )

        totalSlots = cache.get("Slot")
        if totalSlots is None:
            return Response(
                {"message": "No slot found with given slot id", "details": None},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            totalSlots = json.loads(totalSlots)
            for slot in totalSlots:
                if slot["id"] == int(slot_id):
                    return Response(
                        {"message": "Slot details", "details": slot},
                        status=status.HTTP_200_OK,
                    )
            return Response(
                {"message": "No slot found with given slot id", "details": None},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return Response(
            {"message": str(e), "details": None},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
