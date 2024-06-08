import datetime

from django.test import TestCase

from .models import Event, Trip


def create_trip(people_count, title):
    return Trip.objects.create(people_count=people_count, title=title)

def create_event(trip, date, start_time, end_time, title, price, comment, address):
    return Event.objects.create(
        trip=trip,
        date=date,
        start_time=start_time,
        end_time=end_time,
        title=title,
        price=price,
        comment=comment,
        address=address
    )
    
class EventModelTests(TestCase):
    def test_coordinates(self):
        trip = Trip.objects.create(title="Flinston trip")
        current_datetime = datetime.datetime.now(tz=datetime.timezone.utc)
        event = Event.objects.create(trip=trip, lat=20.12345, long=25.12345)
        self.assertEqual(event.coordinates(), "20.12345,25.12345")