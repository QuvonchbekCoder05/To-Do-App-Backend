from django.db import models

from order_and_zayavka.models.delivery_method import (
    DeliveryPrice,
    District,
    PickupPoint,
    Region,
)
from products.models.product import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("process", "Process"),
        ("finished", "Finished"),
        ("rejected", "Rejected"),
    ]
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    comment = models.TextField(blank=True, null=True)  # Foydalanuvchi qoldirgan izoh
    image = models.ImageField(upload_to="order_images/", blank=True, null=True)
    video = models.FileField(upload_to="order_videos/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)
    operator_comment = models.TextField(
        default="pustoy", blank=True, null=True
    )  # Adminning kommentariyasi

    # Yetkazib berish uchun bog‘langan modellar
    delivery_region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True
    )
    delivery_district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, blank=True
    )
    delivery_pickup_point = models.ForeignKey(
        PickupPoint, on_delete=models.SET_NULL, null=True, blank=True
    )
    delivery_price = models.ForeignKey(
        DeliveryPrice, on_delete=models.SET_NULL, null=True, blank=True
    )

    products = models.ManyToManyField(Product, through="OrderProduct")

    def __str__(self):
        return f"{self.name} - {self.status}"
