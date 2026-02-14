from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=29)
    qty = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (qty: {self.qty})"
