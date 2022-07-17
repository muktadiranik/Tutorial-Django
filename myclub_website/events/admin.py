from django.contrib import admin
from .models import Venue
from .models import Event
from .models import MyClubUser
from django.contrib.auth.models import Group

# admin.site.register(Venue)
# admin.site.register(Event)
# admin.site.register(MyClubUser)
admin.site.unregister(Group)



@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "zip_code", "phone", "website", "email_address")
    ordering = ("name", )
    search_fields = ("name", "address")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (("name", "venue"), "event_date", "manager", "description", "attendees")
    list_display = ("name", "venue", "event_date", "manager", "description")
    list_filter = ("event_date", "venue")
    ordering = ("-event_date", )

@admin.register(MyClubUser)
class UserAdmin(admin.ModelAdmin):
    fields = ("first_name", "last_name", "email")
    list_display = ("first_name", "last_name", "email")
    list_display_links = ("first_name", "last_name")
    ordering = ("first_name", )

