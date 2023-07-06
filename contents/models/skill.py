from django.db import models
from django.contrib.auth import settings

from common.models import BaseModel


class Skill(BaseModel, models.Model):

    # name, description, proficiency level,
    PROFICIENCY_LEVEL_CHOICES = [
        ('junior', 'Junior'),
        ('middle', 'Middle'),
        ('senior', 'Senior'),
        ('team lead', 'Team lead'),
    ]

    proficiency_level = models.CharField(
        max_length=20,
        choices=PROFICIENCY_LEVEL_CHOICES,
        default='junior'
    )

    def __str__(self):
        return self.proficiency_level

    class Meta:
        ordering = ["proficiency_level"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
