from django.db import models

from products.models.product import Product


class Discount(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="discount"
    )
    discount_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # % chegirma saqlaymiz
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name_uz} - {self.discount_percent}% chegirma"
