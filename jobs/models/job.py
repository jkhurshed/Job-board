from django.db import models
from django.conf import settings

from uuid import uuid4

from common.models import BaseModel

from contents.models import Location

from employers.models import Company


class Job(BaseModel, models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    salary = models.DecimalField("Salary", max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
