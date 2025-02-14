from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Service(models.Model):
    STATUS_CHOICES = [
        ("faol", "Faol"),
        ("faol_emas", "Faol emas"),
        ("yangi", "Yangi"),
        ("sotilgan", "Sotilgan"),
    ]

    name_uz = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255)
    description_uz = models.TextField(null=True, blank=True)
    description_ru = models.TextField()
    images = models.ManyToManyField("ServiceImage", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="faol")
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            if self.name_uz:
                self.slug = slugify(self.name_uz)
            elif self.name_ru:
                self.slug = slugify(
                    unidecode(self.name_ru)
                )  # ✅ Ruscha harflarni to‘g‘ri aylantiramiz!
            else:
                self.slug = "default-slug"

        super().save(*args, **kwargs)


class ServiceImage(models.Model):
    image = models.ImageField(upload_to="services/")

    def __str__(self):
        return f"Image for {self.service.name_uz}"
