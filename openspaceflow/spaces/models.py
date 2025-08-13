from django.db import models


class Space(models.Model):
    number = models.CharField("Space #", max_length=128)
    info = models.TextField(blank=True, max_length=1024, verbose_name="Description")

    def __str__(self):
        return self.number
