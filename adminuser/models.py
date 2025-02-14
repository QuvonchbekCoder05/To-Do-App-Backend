from django.db import models


class SiteVisitor(models.Model):
    ip_address = models.GenericIPAddressField(
        unique=True
    )  # IP manzil faqat bitta marta oladigan qilingan
    visit_time = models.DateTimeField(auto_now_add=True)  # Saytga tashrif buyurgan vaqt

    def __str__(self):
        return f"{self.ip_address} - {self.visit_time}"
