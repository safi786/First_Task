from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    typ = models.IntegerField(null=True, blank=False)
    user_currency = models.CharField(max_length=30, blank=False)
    money = models.FloatField(null=True, blank=False)
    portfolio_calc = models.FloatField(null=True, blank=False)
    stop_loss_pc = models.IntegerField(null=True, blank=False)
    max_invest_pc = models.IntegerField(null=True, blank=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Asset(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30)
    asset_type_id = models.IntegerField()
    shortable = models.IntegerField()
    active = models.IntegerField()
    news_date = models.DateField()


class UserAsset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)


class Exchange(models.Model):
    asset_type_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)


class UserExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    api_url = models.URLField(null=False, blank=False)
    api_key = models.CharField(max_length=200, null=False, blank=False)
    secret_key = models.CharField(max_length=200, null=False, blank=False)
    portfolio_rest = models.FloatField()
    portfolio_calc = models.FloatField()
