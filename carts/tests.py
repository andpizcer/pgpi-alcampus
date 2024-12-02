from django.test import TestCase
from django.urls import reverse
from accounts.models import Account
from store.models import Product, Variation
from .models import Cart, CartItem

class CartViewTests(TestCase):
    def setUp(self):
        # Crear usuario
        self.user = Account.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            username='john',
            password='securepassword123'
        )
        self.client.login(email='john@example.com', password='securepassword123')

        # Crear producto
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            stock=10,
            description='A product for testing'
        )
        
        # Crear carrito
        self.cart = Cart.objects.create(cart_id='test_cart')

        # Crear variación
        self.variation = Variation.objects.create(
            product=self.product,
            variation_category='color',
            variation_value='red',
            is_active=True
        )
        
        self.cart_item_data = {
            'product_id': self.product.id,
            'quantity': 2,
            'variation': [self.variation.id]
        }

    def test_add_to_cart_success(self):
        response = self.client.post(reverse('add_to_cart'), self.cart_item_data)
        self.assertEqual(response.status_code, 302)  # Redirige tras añadir al carrito
        self.assertTrue(CartItem.objects.filter(product=self.product, cart=self.cart).exists())
        cart_item = CartItem.objects.get(product=self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertTrue(cart_item.is_active)

    def test_add_to_cart_with_variation(self):
        response = self.client.post(reverse('add_to_cart'), self.cart_item_data)
        self.assertEqual(response.status_code, 302)
        cart_item = CartItem.objects.get(product=self.product)
        self.assertIn(self.variation, cart_item.variation.all())

    def test_remove_from_cart(self):
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1,
            is_active=True
        )
        response = self.client.post(reverse('remove_from_cart'), {'item_id': cart_item.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    def test_sub_total_calculation(self):
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=3,
            is_active=True
        )
        self.assertEqual(cart_item.sub_total(), self.product.price * 3)
