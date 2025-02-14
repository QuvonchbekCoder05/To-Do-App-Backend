from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from .attribute import Attribute
from .brand import Brand
from .category import Category
from .type import Type


class Product(models.Model):
    STATUS_CHOICES = [
        ("faol", "Faol"),
        ("faol_emas", "Faol emas"),
        ("yangi", "Yangi"),
        ("sotilgan", "Sotilgan"),
        ("discounted", "Chegirma"),
    ]

    name_uz = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name_ru = models.CharField(max_length=255, unique=True)
    description_uz = models.TextField(unique=True, null=True, blank=True)
    description_ru = models.TextField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="faol")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="products")
    attributes = models.ManyToManyField(Attribute, blank=True)
    images = models.ImageField(upload_to="product_images/", blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            if self.name_uz:
                self.slug = slugify(self.name_uz)
            elif self.name_ru:
                self.slug = slugify(unidecode(self.name_ru))
            else:
                self.slug = "default-slug"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name_uz or self.name_ru} - {self.description_uz or self.description_ru}"
