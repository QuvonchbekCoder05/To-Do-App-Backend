from django.db import models


class Category(models.Model):
    name_uz = models.CharField(max_length=255, null=True, blank=True, unique=True)
    name_ru = models.CharField(max_length=255, unique=True)
