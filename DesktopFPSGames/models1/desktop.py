from django.db import models

from .attributes import DesktopAttributes
from .desktop_type import DesktopType

STATUS_CHOICES = [
    ("faol", "Faol"),
    ("faol_emas", "Faol emas"),
    ("yangi", "Yangi"),
    ("sotilgan", "Sotilgan"),
]


class Desktop(models.Model):
    name_uz = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255)
    description_uz = models.TextField(null=True, blank=True)
    description_ru = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="yangi")
    images = models.ManyToManyField("Image", blank=True)
    type = models.ForeignKey(
        DesktopType, on_delete=models.CASCADE, related_name="desktops"
    )
    attributes = models.ManyToManyField(
        DesktopAttributes, blank=True, related_name="desktops"
    )

    def __str__(self):
        return f"{self.name_uz or self.name_ru} - {self.description_uz or self.description_ru}"


class Image(models.Model):
    image = models.ImageField(upload_to="desktop_images/")
