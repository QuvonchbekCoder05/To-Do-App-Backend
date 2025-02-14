from django.db import models


class Type(models.Model):
    name_uz = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name_ru = models.CharField(max_length=255, unique=True)
