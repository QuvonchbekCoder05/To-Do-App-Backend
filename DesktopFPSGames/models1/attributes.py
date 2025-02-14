from django.db import models
from django.utils.text import slugify


class DesktopAttributes(models.Model):
    key_uz = models.CharField(max_length=255, null=True, blank=True)
    key_ru = models.CharField(max_length=255)
    value_uz = models.TextField(null=True, blank=True)
    value_ru = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.key_uz or self.key_ru} - {self.value_uz or self.value_ru}"
