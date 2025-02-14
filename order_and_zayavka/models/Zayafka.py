from django.db import models


# Foydalanuvchilar qoldirgan zayavka modeli
class Zayafka(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("process", "Process"),
        ("finished", "Finished"),
        ("rejected", "Rejected"),
    ]
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    def __str__(self):
        return f"{self.name} - {self.status}"
