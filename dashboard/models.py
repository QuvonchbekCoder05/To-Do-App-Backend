from django.db import models


class SiteVisit(models.Model):
    ip_address = models.GenericIPAddressField(
        unique=True
    )  # Foydalanuvchi IP-manzilini saqlaymiz
    timestamp = models.DateTimeField(auto_now_add=True)  # Tashrif vaqtini saqlaymiz

    def __str__(self):
        return self.ip_address
