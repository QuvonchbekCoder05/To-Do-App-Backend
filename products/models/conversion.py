from django.db import models


class Conversion(models.Model):
    som_value = models.DecimalField(max_digits=7, decimal_places=2, default=12000)

    def __str__(self):
        return f"1 USD = {self.som_value} UZS"
