from django.contrib import admin
from .models import AdditionalUserInfo

@admin.register(AdditionalUserInfo)
class AdditionalUserInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "birthday", "address", "zip_code", "phone", "website", "bio")
    fields = ("user", "birthday", "address", "zip_code", "phone", "website", "bio", "user_image")
    ordering = ("user", )
    search_fields = ("phone", "website")
