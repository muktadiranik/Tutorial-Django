from django.db import models
from django.contrib.auth.models import User

class AdditionalUserInfo(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    birthday = models.DateField()
    address = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    user_image = models.ImageField(upload_to="images/", blank=True, null=True)
