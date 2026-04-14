from django.db import models
from .constants import ItemConstraints


class Item(models.Model):
    name = models.CharField(max_length=ItemConstraints.NAME_MAX_LENGTH, unique=True)
    qty = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (qty: {self.qty})"

    @property
    def is_out_of_stock(self):
        return self.qty == 0

    @property
    def is_low_stock(self):
        return not self.is_out_of_stock and self.qty <= self.reorder_level
