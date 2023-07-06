from django.db import models


class Applicant(models.Model):

    name = models.CharField('Applicant name', max_length=100)
    skill = models.ForeignKey("contents.Skill", on_delete=models.CASCADE)
    user = models.ForeignKey("users_app.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Applicant"
        verbose_name_plural = "Applicants"
        ordering = ['name']
