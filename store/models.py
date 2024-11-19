from itertools import product
from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg


    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    def is_stock_low(self):
        return self.stock < 10 
    
    def notify_low_stock(sender, instance, **kwargs):
     if instance.is_stock_low():
        send_mail(
            'Alerta de Stock Bajo',
            f'El producto {instance.name} tiene un stock de {instance.stock}.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

    post_save.connect(notify_low_stock, sender=product)



class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def tallas(self):
        return super(VariationManager, self).filter(variation_category='talla', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('talla', 'talla'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()


    def __str__(self):
        return self.variation_category + ' : ' + self.variation_value


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Calificación de 1 a 5
    comment = models.TextField(blank=True, null=True)  # Comentario opcional
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación

    def __str__(self):
        return f"{self.rating} estrellas por {self.user.username} para {self.product.name}"

    class Meta:
        ordering = ['-created_at']   
        unique_together = ('product', 'user') 


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name
