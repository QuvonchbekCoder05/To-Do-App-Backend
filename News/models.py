from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

STATUS_CHOICES = [
    ("faol", "Faol"),
    ("faol_emas", "Faol emas"),
    ("yangi", "Yangi"),
    ("rasprodaja", "Rasprodaja"),
]


class News(models.Model):
    name_uz = models.CharField(max_length=255, null=True, blank=True)
    name_ru = models.CharField(max_length=255)
    description_uz = models.TextField(null=True, blank=True)
    description_ru = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="yangi")
    slug = models.SlugField(blank=True)
    images = models.ManyToManyField("Image", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            if self.name_uz:
                self.slug = slugify(self.name_uz)
            elif self.name_ru:
                self.slug = slugify(
                    unidecode(self.name_ru)
                )  # ✅ To‘g‘ri transliteratsiya!
            else:
                self.slug = "default-slug"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz if self.name_uz else self.name_ru


class Image(models.Model):
    image = models.ImageField(upload_to="news_images/")
