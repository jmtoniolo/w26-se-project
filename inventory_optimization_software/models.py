from django.db import models
from .constants import ItemConstraints


class Item(models.Model):
    name = models.CharField(max_length=ItemConstraints.NAME_MAX_LENGTH)
    qty = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (qty: {self.qty})"
