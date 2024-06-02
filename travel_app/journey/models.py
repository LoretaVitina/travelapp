import os

import requests
from django.db import models


class Trip(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    people_count = models.IntegerField(default=1)
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title

class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField()
    address = models.CharField(max_length=200)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return self.title
    
    def save(self, **kwargs):
        api_key = os.environ['GOOGLE_MAPS_APIKEY']
        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(self.address, api_key)).json()
        if api_response['status'] == 'OK':
            self.long = api_response["results"][0]["geometry"]['location']['lng']
            self.lat = api_response["results"][0]["geometry"]['location']['lat']
        else:
            self.long = 0.0
            self.lat = 0.0
        super().save(**kwargs)