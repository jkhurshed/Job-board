from django.db import models

from common.models import UUIDmodel


class Location(UUIDmodel, models.Model):

    country = models.CharField("Country", max_length=100)
    state = models.CharField("State or region", max_length=100)
    city = models.CharField("City", max_length=100)
    address = models.CharField("Address", max_length=250)

    def __str__(self):
        return self.address

    class Meta:
        ordering = ['country']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
