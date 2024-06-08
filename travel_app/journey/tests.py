import datetime

from django.test import TestCase

from .models import Event, Trip


class EventModelTests(TestCase):
    def test_coordinates(self):
        trip = Trip.objects.create(title="Flinston trip")
        event = Event.objects.create(trip=trip, lat=20.12345, long=25.12345)
        self.assertEqual(event.coordinates(), "20.12345,25.12345")