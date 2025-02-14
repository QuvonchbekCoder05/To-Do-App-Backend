from django.db import models


class Attribute(models.Model):
    key_uz = models.CharField(max_length=255, blank=True, null=True)
    key_ru = models.CharField(max_length=255, blank=True, null=True)
    value_uz = models.CharField(max_length=255, blank=True, null=True)
    value_ru = models.CharField(max_length=255, blank=True, null=True)
