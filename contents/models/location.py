from django.db import models

from common.models import UUIDmodel


class Location(UUIDmodel, models.Model):
    
   # country, state, city, address,

    country = models.CharField("Country", max_length=100)
    state = models.CharField("State or region", max_length=100)
    city = models.CharField("City", max_length=100)
    adress = models.CharField("Adress", max_length=250)

    class Meta:
        verbose_name= 'Location'
        verbose_name_plural = 'Locations'
        ordering = ['title']