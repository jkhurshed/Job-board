from django.db import models


class CreateUpdatetimeModel(models.Model):
    """
    Abstact model with create and update time ordered by create time
    """
    create_time = models.DateTimeField("Date created", auto_now_add=True)
    update_time = models.DateTimeField("Date updated", auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-create_time']
