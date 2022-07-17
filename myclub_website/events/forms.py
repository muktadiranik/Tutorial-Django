from django import forms
from django.forms import ModelForm
from .models import Venue
from .models import MyClubUser
from .models import Event

# create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # fields = "__all__"
        fields = ("name", "address", "zip_code", "phone", "website", "email_address" , "venue_image")

        labels = {
            "name": "",
            "address": "",
            "zip_code": "",
            "phone": "",
            "website": "",
            "email_address": "",
            "venue_image": "",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Zip Code"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"}),
            "website": forms.TextInput(attrs={"class": "form-control", "placeholder": "Website"}),
            "email_address": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
        }

# create an event form for SuperUser
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ("name", "event_date", "venue", "manager", "description", "attendees")
        labels = {
            "name": "",
            "event_date": "YYYY-MM-DD HH:MM:SS",
            "venue": "Venue",
            "manager": "Manager",
            "description": "",
            "attendees": "Attendees",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
            "event_date": forms.DateTimeInput(attrs={"class": "form-control", "placeholder": "Event Date", "type": "datetime-local"}),
            "venue": forms.Select(attrs={"class": "form-select", "placeholder": "Venue"}),
            "manager": forms.Select(attrs={"class": "form-select", "placeholder": "Manager"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "attendees": forms.SelectMultiple(attrs={"class": "form-control", "placeholder": "Attendees"}),
        }


# create an event form for user
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ("name", "event_date", "venue", "description", "attendees")
        labels = {
            "name": "",
            "event_date": "",
            "venue": "Venue",
            "description": "",
            "attendees": "Attendees",
        }

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
            "event_date": forms.DateTimeInput(attrs={"class": "form-control", "placeholder": "Event Date", "type": "datetime-local"}),
            "venue": forms.Select(attrs={"class": "form-select", "placeholder": "Venue"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Description"}),
            "attendees": forms.SelectMultiple(attrs={"class": "form-control", "placeholder": "Attendees"}),
        }

# create a user form
class UserForm(ModelForm):
    class Meta:
        model = MyClubUser
        fields = "__all__"

        labels = {
            "first_name": "",
            "last_name": "",
            "email": ""
        }

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"})
        }
