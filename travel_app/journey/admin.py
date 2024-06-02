from django.contrib import admin

from .models import Event, Trip


class EventInline(admin.StackedInline):
    model = Event
    extra = 0
    fieldsets = [
        ("Event base data", {"fields": ["title", "date"]}),
        ("Event details", {"fields": ["start_time", "end_time", "price", "address"]}),
        ("Extra information", {"fields": ["comment"], "classes": ["collapse"]})
    ] 

class TripAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Trip base data", {"fields": ["title", "people_count"]})
    ] 
    inlines = [EventInline]

admin.site.register(Trip, TripAdmin)
