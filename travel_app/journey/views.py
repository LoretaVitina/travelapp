from django.shortcuts import render
from django.views import generic

from .models import Event, Trip


class IndexView(generic.ListView):
    template_name = "journey/index.html"
    context_object_name = "trips"
    
    def get_queryset(self):
        return Trip.objects.order_by("created_at")
    
