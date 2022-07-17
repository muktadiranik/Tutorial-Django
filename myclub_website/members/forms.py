from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import AdditionalUserInfo
from django.forms import ModelForm


class AdditionalUserInfoForm(ModelForm):
    class Meta:
        model = AdditionalUserInfo
        fields = ("birthday", "address", "zip_code", "phone", "website", "bio", "user_image")
        labels = {
            "birthday": "",
            "address": "",
            "zip_code": "",
            "phone": "",
            "website": "",
            "bio": "",
            "user_image": "",
        }
        widgets = {
            "birthday": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Address"}),
            "zip_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "ZIP Code"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"}),
            "website": forms.TextInput(attrs={"class": "form-control", "placeholder": "Website"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "placeholder": "Bio"}),
        }


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Type Password"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Retype Password"
