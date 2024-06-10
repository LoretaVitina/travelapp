from django.shortcuts import render
from django.views import generic

from .models import Trip


class IndexView(generic.ListView):
    template_name = "journey/index.html"
    context_object_name = "trips"
    
    def get_queryset(self):
        return Trip.objects.order_by("created_at")
    
    
class DetailView(generic.DetailView):
    model = Trip
    template_name = "journey/detail.html"