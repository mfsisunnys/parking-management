from django.test import TestCase
import unittest
from django.test import Client
from django.urls import reverse

# Create your tests here.

client = Client()


class SlotTestCase(TestCase):
    def setUp(self):
        response = client.post(reverse('parkingLot'), {'name': 'Test Parking Lot'})
        self.assertEqual(response.status_code, 200)

    def test_park_vehicle(self):
        response = client.post(reverse('park'), {'vehicle_number': 'DL-01-HH-1234'})
        self.assertEqual(response.status_code, 200)


    def test_slot_if_available(self):
        response = client.get(reverse('get_slot_detail')+ '?slot_id=1') 
        self.assertEqual(response.status_code, 200)

    def test_slot_if_not_available(self):
        response = client.get(reverse('get_slot_detail')+ '?slot_id=7')
        self.assertEqual(response.status_code, 400)


    

    