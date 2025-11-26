from django.db import models
from django.contrib.auth.models import User
from dublindistance import calculate_distance  # your library

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)
    delivery_distance_km = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Use your own library when saving the order
        if not self.delivery_distance_km:
            # Example: distance from Dublin to customer city (you can make it dynamic later)
            self.delivery_distance_km = calculate_distance("Dublin", "Galway")  # or use real input
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} – {self.product.name} × {self.quantity}"