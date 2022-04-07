from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from encrypted_model_fields.fields import EncryptedCharField
User._meta.get_field('email')._unique = True


# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30)

    def __str__(self):
        return "%s (%s)" % (self.name, self.symbol)
class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=30)
    asset_type_id = models.IntegerField()
    shortable = models.IntegerField()
    active = models.IntegerField()
    news_date = models.DateField()
    def __str__(self):
        return "%s (%s)" % (self.name, self.symbol)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    typ = models.IntegerField(null=True, blank=True)
    user_currency = models.CharField(max_length=30, blank=True)
    money = models.FloatField(null=True, blank=True)
    portfolio_calc = models.FloatField(null=True, blank=True)
    stop_loss_pc = models.IntegerField(null=True, blank=True)
    max_invest_pc = models.IntegerField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s" % (self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# class UserAsset(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     asset = models.ForeignKey(Asset, on_delete=models.CASCADE)


class Exchange(models.Model):
    asset_type_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return "%s (%s)" % (self.name, self.asset_type_id)

class UserExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    api_url = models.URLField(null=False, blank=True)
    api_key = EncryptedCharField(max_length=200, null=False, blank=True)
    secret_key = EncryptedCharField(max_length=200, null=False, blank=True)
    portfolio_rest = models.FloatField(null=True, blank=True)
    portfolio_calc = models.FloatField(null=True, blank=True)
    def __str__(self):
        return "%s (%s)" % (self.exchange.name, self.user.username)