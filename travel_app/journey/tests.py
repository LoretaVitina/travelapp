import datetime
import os
from decimal import Decimal

import mock
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Event, Trip


class EventModelTests(TestCase):
    def create_trip(self):
        return Trip.objects.create(title="Flinston trip")
    
    def test_coordinates(self):
        trip = self.create_trip()
        event = Event.objects.create(trip=trip, lat=20.12345, long=25.12345)
        self.assertEqual(event.coordinates(), "20.12345,25.12345")
        
    def test_costs_is_not_negative_validator(self):
        trip = self.create_trip()
        event = Event.objects.create(trip=trip, price=-50.00)
        self.assertRaises(ValidationError, event.full_clean)
        
class TripModelTests(TestCase):
    def create_trip(self):
        return Trip.objects.create(title="Big Flight trip")
    
    def test_costs(self):
        trip = self.create_trip()
        Event.objects.create(trip=trip, price=50.12)
        Event.objects.create(trip=trip, price=50.00)
        self.assertEqual(trip.costs(),Decimal('100.12'))
        
    def test_costs_per_person(self):
        trip = Trip.objects.create(title="Big Flight trip", people_count=5)
        Event.objects.create(trip=trip, price=50.55)
        self.assertEqual(trip.costs_per_person(),Decimal('10.11'))
        
    def test_start_date(self):
        trip = self.create_trip()
        Event.objects.create(trip=trip, date=datetime.date(2024, 1, 1))
        Event.objects.create(trip=trip, date=datetime.date(2024, 3, 4))
        Event.objects.create(trip=trip, date=datetime.date(2024, 6, 10))
        self.assertEqual(trip.start_date(),datetime.date(2024, 1, 1))
    
    def test_end_date(self):
        trip = self.create_trip()
        Event.objects.create(trip=trip, date=datetime.date(2024, 1, 1))
        Event.objects.create(trip=trip, date=datetime.date(2024, 3, 4))
        Event.objects.create(trip=trip, date=datetime.date(2024, 6, 10))
        self.assertEqual(trip.end_date(),datetime.date(2024, 6, 10))
        
    def test_duration(self):
        trip = self.create_trip()
        Event.objects.create(trip=trip, date=datetime.date(2024, 1, 1))
        Event.objects.create(trip=trip, date=datetime.date(2024, 1, 10))
        self.assertEqual(trip.duration(), 10)
        
    def test_all_coordinates(self):
        trip = self.create_trip()
        Event.objects.create(trip=trip, lat=55.9032181, long=26.9894481)
        Event.objects.create(trip=trip, lat=55.8826088, long=26.5464623)
        Event.objects.create(trip=trip, lat=56.7241912, long=24.2010674)
        self.assertEqual(trip.all_coordinates(), '55.903218,26.989448|55.882609,26.546462|56.724191,24.201067')
        
    @mock.patch.dict(os.environ, {"GOOGLE_MAPS_APIKEY": "manaslepenaatslega"})    
    def test_map_url(self):
        trip = self.create_trip()
        Event.objects.create(trip=trip, lat=55.9032181, long=26.9894481)
        Event.objects.create(trip=trip, lat=55.8826088, long=26.5464623)
        self.assertEqual(trip.map_url(), 'https://maps.googleapis.com/maps/api/staticmap?size=640x640&maptype=roadmap&markers=color:blue%7C55.903218,26.989448|55.882609,26.546462&key=manaslepenaatslega')