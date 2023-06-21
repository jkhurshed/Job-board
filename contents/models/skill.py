from django.db import models

from common.models import BaseModel

class Skill(BaseModel, models.Model):

    # name, description, proficiency level,
    class Meta:
        ordering = ["title"]