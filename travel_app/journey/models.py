import datetime
import os

import django
import requests
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Max, Min, Sum


class Trip(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    people_count = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/uploaded', default='images/default.jpg')
    
    def __str__(self):
        return self.title
    
    def costs(self):
        return self.event_set.aggregate(Sum('price'))['price__sum']
    
    def costs_per_person(self):
        return self.costs() / self.people_count
    
    def start_date(self):
        return self.event_set.aggregate(Min('date'))['date__min']
    
    def end_date(self):
        return self.event_set.aggregate(Max('date'))['date__max']
    
    def duration(self):
        return (self.end_date() - self.start_date()).days + 1
    
    def days_from_updated_at(self):
        return (datetime.datetime.now(tz=datetime.timezone.utc) - self.updated_at).days
    
    def all_coordinates(self):
        return "|".join(event.coordinates() for event in self.event_set.all())
    
    def map_url(self):
        return "https://maps.googleapis.com/maps/api/staticmap?size=640x640&maptype=roadmap&markers=color:blue%7C" + self.all_coordinates() + "&key=" + os.environ['GOOGLE_MAPS_APIKEY']

class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    start_time = models.DateTimeField(default=django.utils.timezone.now)
    end_time = models.DateTimeField(default=django.utils.timezone.now)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0)])
    comment = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=200)
    long = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    
    def __str__(self):
        return self.title
    
    def save(self, **kwargs):
        api_key = os.environ.get('GOOGLE_MAPS_APIKEY')
        if api_key != None:
            api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(self.address, api_key)).json()
            if api_response['status'] == 'OK':
                self.long = api_response["results"][0]["geometry"]['location']['lng']
                self.lat = api_response["results"][0]["geometry"]['location']['lat']
        super().save(**kwargs)
        
    def coordinates(self):
        return str(self.lat) + "," + str(self.long)