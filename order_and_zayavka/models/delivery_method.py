from django.db import models


# ✅ 1️⃣ Viloyatlar modeli
class Region(models.Model):
    name_uz = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name_ru = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField(null=True, blank=True)  # 🆕 Qo‘shildi
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name_uz


# ✅ 2️⃣ Tumanlar modeli (Viloyatga bog‘langan)
class District(models.Model):
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="districts"
    )
    name_uz = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name_ru = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.region.name_uz} - {self.name_uz}"


# ✅ 3️⃣ Olib ketish punktlari (Tuman ichida)
class PickupPoint(models.Model):
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="pickup_points"
    )
    address_uz = models.CharField(max_length=255, null=True, blank=True)
    address_ru = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)  # 🆕 Qo‘shildi
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.district.name_uz} - {self.address_uz}"


# ✅ 4️⃣ Yetkazib berish narxlari (Viloyatga bog‘langan)
class DeliveryPrice(models.Model):
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="delivery_prices"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_time = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.region.name_uz} - {self.price} UZS"


# ✅ 5️⃣ Yetkazib berish manzillari (Foydalanuvchi uchun)
class DeliveryAddress(models.Model):
    order = models.OneToOneField(
        "order_and_zayavka.Order",
        on_delete=models.CASCADE,
        related_name="delivery_address",
    )
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.TextField(unique=True)

    def __str__(self):
        return f"{self.order.name} - {self.address}"
