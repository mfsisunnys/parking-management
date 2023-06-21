from django.core.cache import cache

from decouple import config
import json
import hashlib

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import AnonRateThrottle

from authentication_management.authentication import token_required


# Create your views here.

total_slots = config("TOTAL_SLOTS")


def check_existing_vehicle(vehicle_number):
    totalSlots = cache.get("Slot")
    if totalSlots is None:
        return False
    else:
        totalSlots = json.loads(totalSlots)
        for slot in totalSlots:
            if slot["vehicle_number"] == vehicle_number:
                return True, slot["id"]
        return False, None


@token_required
@throttle_classes([AnonRateThrottle])
@api_view(["POST"])
def parkingLot(request, auth):
    """
    This function creates a parking lot which takes in parking lot name as input and returns the parking lot id
    """
    try:
        if auth:
            name = request.data.get("name")
            if name is None or name == "":
                return Response(
                    {"message": "Please provide parking lot name", "details": None},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate parking lot id
            hashObj = hashlib.md5(name.encode())
            id = hashObj.hexdigest()

            parking_lot_dict = {"id": id, "name": name}
            cache.set("ParkingLot", json.dumps([parking_lot_dict]))
            return Response(
                {
                    "message": "Parking lot created successfully",
                    "details": parking_lot_dict,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Invalid token", "details": None},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    except Exception as e:
        return Response(
            {"message": "Something went wrong", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@token_required
@throttle_classes([AnonRateThrottle])
@api_view(["POST"])
def park(request, auth):
    """
    This function parks a vehicle which takes in vehicle number as input and returns the slot number in which the vehicle is parked
    """
    try:
        if auth:
            vehicle_number = request.data.get("vehicle_number")
            parking_lot = cache.get("ParkingLot")
            is_occupied = True
            parking_lot_id = json.loads(parking_lot)[0]["id"]

            if vehicle_number is None or vehicle_number == "":
                return Response(
                    {"message": "Please provide vehicle number", "details": None},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if parking_lot is None or parking_lot == "":
                return Response(
                    {"message": "Please create a parking lot first", "details": None},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            totalSlots = cache.get("Slot")
            if totalSlots is None:
                slot_id = 1
                new_slot_dict = {
                    "id": slot_id,
                    "vehicle_number": vehicle_number,
                    "is_occupied": is_occupied,
                    "parking_lot_id": parking_lot_id,
                }
                cache.set("Slot", json.dumps([new_slot_dict]))
                return Response(
                    {
                        "message": f"Vehicle parked in slot {slot_id}",
                        "details": new_slot_dict,
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                totalSlots = json.loads(totalSlots)
                current_slots = len(totalSlots)
                vehicle_exists, slot_id = check_existing_vehicle(vehicle_number)
                if vehicle_exists == False:
                    if current_slots < int(total_slots):
                        slot_id = current_slots + 1
                        current_slot_info = totalSlots
                        new_slot_dict = {
                            "id": slot_id,
                            "vehicle_number": vehicle_number,
                            "is_occupied": is_occupied,
                            "parking_lot_id": parking_lot_id,
                        }
                        current_slot_info.append(new_slot_dict)
                        cache.set("Slot", json.dumps(current_slot_info))
                        return Response(
                            {
                                "message": f"Vehicle parked in slot {slot_id}",
                                "details": new_slot_dict,
                            },
                            status=status.HTTP_200_OK,
                        )

                    else:
                        for slot in totalSlots:
                            if slot["is_occupied"] == False:
                                slot["vehicle_number"] = vehicle_number
                                slot["is_occupied"] = True
                                cache.set("Slot", json.dumps(totalSlots))
                                return Response(
                                    {
                                        "message": f'Vehicle parked in slot {slot["id"]}',
                                        "details": slot,
                                    },
                                    status=status.HTTP_200_OK,
                                )
                        return Response(
                            {"message": "Parking lot is full", "details": None},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                else:
                    return Response(
                        {
                            "message": f"Vehicle already parked in slot {slot_id}",
                            "details": None,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        else:
            return Response(
                {"message": "Invalid token", "details": None},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except Exception as e:
        return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@token_required
@throttle_classes([AnonRateThrottle])
@api_view(["PUT"])
def unpark(request, auth):
    """
    This function unparks a vehicle from a slot taking vehicle number as input and returns the slot number
    """
    try:
        if auth:
            vehicle_number = request.data.get("vehicle_number")
            if vehicle_number is None or vehicle_number == "":
                return Response(
                    {"message": "Please provide vehicle number", "details": None},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            totalSlots = cache.get("Slot")
            if totalSlots is None:
                return Response(
                    {"message": "No vehicles parked", "details": None},
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                totalSlots = json.loads(totalSlots)
                for slot in totalSlots:
                    if slot["vehicle_number"] == vehicle_number:
                        slot["vehicle_number"] = None
                        slot["is_occupied"] = False
                        cache.set("Slot", json.dumps(totalSlots))
                        return Response(
                            {
                                "message": f'Vehicle unparked from {slot["id"]}',
                                "details": slot,
                            },
                            status=status.HTTP_200_OK,
                        )
                return Response(
                    {
                        "message": f"Vehicle not found for given number {vehicle_number}",
                        "details": None,
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )
        else:
            return Response(
                {"message": "Invalid token", "details": None},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except Exception as e:
        return Response(
            {"message": str(e), "details": None},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
