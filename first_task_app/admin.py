from django.contrib import admin
from .models import *


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields if field.name != "id"]
    list_filter = [field.name for field in Profile._meta.fields if field.name != "id"]


class LanguageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Language._meta.fields if field.name != "id"]
    list_filter = [field.name for field in Language._meta.fields if field.name != "id"]


class AssetAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Asset._meta.fields if field.name != "id"]
    list_filter = [field.name for field in Asset._meta.fields if field.name != "id"]


class ExchangeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Exchange._meta.fields if field.name != "id"]
    list_filter = [field.name for field in Exchange._meta.fields if field.name != "id"]


class UserExchangeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserExchange._meta.fields if field.name != "id"]
    list_filter = [field.name for field in UserExchange._meta.fields if field.name != "id"]


class UserAssetAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserAsset._meta.fields if field.name != "id"]
    list_filter = [field.name for field in UserAsset._meta.fields if field.name != "id"]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(UserAsset, UserAssetAdmin)
admin.site.register(UserExchange, UserExchangeAdmin)
