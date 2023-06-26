from django.db import models

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

    class Meta:
        ordering = ["proficiency_level"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
