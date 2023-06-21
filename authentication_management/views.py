from django.shortcuts import render

# Create your views here.

from django.core.cache import cache
from django.core.serializers import deserialize
from decouple import config
import json
import jwt

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import AnonRateThrottle

from .authentication import token_required

# Create your views here.


@throttle_classes([AnonRateThrottle])
@api_view(["POST"])
def register(request):
    """
    This function registers a user given username and password
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or username == "" or password is None or password == "":
        return Response(
            {"message": "Please provide username and password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = {"username": username, "password": password}

    user_data = cache.get("userObj")
    if user_data is not None:
        user_data = json.loads(user_data)
        for user_i in user_data:
            if user_i["username"] == username:
                return Response(
                    {"message": "User already exists"},
                    status=status.HTTP_409_CONFLICT,
                )
        else:
            user_data.append(user)
            cache.set("userObj", json.dumps(user_data))
            return Response(
                {"message": "User created successfully", "details": user},
                status=status.HTTP_201_CREATED,
            )
    else:
        cache.set("userObj", json.dumps([user]))
        return Response(
            {"message": "User created successfully", "details": user},
            status=status.HTTP_200_OK,
        )


@throttle_classes([AnonRateThrottle])
@api_view(["POST"])
def login(request):
    """
    This function logs in a user given username and password and returns a token
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or username == "" or password is None or password == "":
        return Response(
            {"message": "Please provide username and password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    userdata = cache.get("userObj")
    if userdata is None:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        user_data = json.loads(userdata)
        for user in user_data:
            if user["username"] == username and user["password"] == password:
                token = jwt.encode(
                    {"username": username}, config("SECRET_KEY"), algorithm="HS256"
                )
                return Response({"token": token}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "User not found/Invalid credentials"},
                status=status.HTTP_404_NOT_FOUND,
            )
