from django.db import models


class Space(models.Model):
    number = models.IntegerField("Space #", unique=True)
    info = models.TextField(blank=True, max_length=1024, verbose_name="Description")

    def __str__(self):
        return f"{self.number}"
