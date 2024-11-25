from django.db import models
from store.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Se refiere al modelo personalizado de usuario.
        on_delete=models.CASCADE,
        null=True,  # Esto permite que el usuario sea opcional (usuarios anónimos).
        blank=True,  # Permite dejar el campo vacío.
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.product_name} ({self.quantity})"