from django.db import models

# Create your models here.
class StudentClub(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False,)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=50)
    landLine = models.CharField(max_length=50)
    address = models.TextField(max_length=50)
    city = models.CharField(max_length=50)
