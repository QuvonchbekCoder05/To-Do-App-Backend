from django.db import models

from order_and_zayavka.models.order import Order
from products.models.product import Product


# Buyurtmadagi mahsulotlar modeli
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order.name} - {self.product.name_uz} ({self.quantity})"
