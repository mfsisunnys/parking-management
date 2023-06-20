from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@api_view(["GET"])
def get_json_schema(request):
    file_path = os.path.join(BASE_DIR, "docs/API_doc/v1/swagger.json")

    try:
        with open(file_path) as file:
            json_data = json.load(file)
            return Response(json_data, status=200)
    except FileNotFoundError:
        return Response({"error": "File not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

