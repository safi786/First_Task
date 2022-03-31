from django.contrib import admin
from .models import *


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields if field.name != "id"]
    list_filter = [field.name for field in Profile._meta.fields if field.name != "id"]


admin.site.register(Profile, ProfileAdmin)
