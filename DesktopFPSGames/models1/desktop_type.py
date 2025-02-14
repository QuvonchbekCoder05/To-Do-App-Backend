from django.db import models


class DesktopType(models.Model):
    name_uz = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255)

    def __str__(self):
        return self.name_uz if self.name_uz else self.name_ru
