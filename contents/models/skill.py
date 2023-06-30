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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    class Meta:
        ordering = ["proficiency_level"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
