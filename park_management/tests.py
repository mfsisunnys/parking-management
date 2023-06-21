from django.test import TestCase
import unittest
from django.test import Client
from django.urls import reverse

from django.core.cache import cache

# Create your tests here.
client = Client()


class ParkingLotTestCase(TestCase):
    def test_parking_lot_creation(self):
        response = client.post(reverse("parkingLot"), {"name": "Test Parking Lot"})
        self.assertEqual(response.status_code, 200)

    def test_parking_lot_creation_with_no_name(self):
        response = client.post(reverse("parkingLot"), {})
        self.assertEqual(response.status_code, 400)

    def test_parking_lot_creation_with_empty_name(self):
        response = client.post(reverse("parkingLot"), {"name": ""})
        self.assertEqual(response.status_code, 400)


class ParkTestCase(TestCase):
    def setUp(self):
        response = client.post(reverse("parkingLot"), {"name": "Test Parking Lot"})
        self.assertEqual(response.status_code, 200)

    def test_park_vehicle(self):
        response = client.post(reverse("park"), {"vehicle_number": "DL-01-HH-1234"})
        self.assertEqual(response.status_code, 200)

    def test_park_vehicle_with_no_vehicle_number(self):
        response = client.post(reverse("park"), {})
        self.assertEqual(response.status_code, 400)

    def test_park_vehicle_with_empty_vehicle_number(self):
        response = client.post(reverse("park"), {"vehicle_number": ""})
        self.assertEqual(response.status_code, 400)

    def test_park_vehicle_with_existing_vehicle_number(self):
        response = client.post(reverse("park"), {"vehicle_number": "KA-01-HH-1234"})
        self.assertEqual(response.status_code, 200)


class UnparkTestCase(TestCase):
    def setUp(self):
        response = client.post(reverse("parkingLot"), {"name": "Test Parking Lot"})
        self.assertEqual(response.status_code, 200)

    def test_park_vehicle(self):
        response = client.post(reverse("park"), {"vehicle_number": "DL-01-HH-1234"})
        self.assertEqual(response.status_code, 200)

    def test_unpark_vehicle(self):
        vehicle_number = "DL-01-HH-1234"
        response = self.client.put(
            reverse("unpark"),
            {"vehicle_number": vehicle_number},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_unpark_vehicle_with_wrong_vehicle_number(self):
        response = client.put(
            reverse("unpark"),
            {"vehicle_number": "DL-01-HH-1235"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 204)

    def test_unpark_vehicle_with_no_vehicle_number(self):
        response = client.put(reverse("unpark"), {}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def cache_clear(self):
        cache.clear()
