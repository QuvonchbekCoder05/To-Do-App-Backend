from django.db import models


class TestAttribute(models.Model):
    key_uz = models.CharField(max_length=255, blank=True, null=True)
    key_ru = models.CharField(max_length=255, blank=True, null=True)
    value_uz = models.CharField(max_length=255, blank=True, null=True)
    value_ru = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.key_uz or self.key_ru}: {self.value_uz or self.value_ru}"
