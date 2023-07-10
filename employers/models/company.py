from django.db import models

from common.models import BaseModel

from contents.models import Location


class Company(BaseModel, models.Model):
    website = models.URLField("Link to website", max_length=250, blank=True)
    logo = models.ImageField(upload_to='static/images/', max_length=200, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
