from django.test import TestCase
from django.urls import reverse

from category.models import Category
from store.models import Product
from carts.models import Cart, CartItem
from orders.models import Order
from accounts.models import UserProfile, Account


class IntegrationTests(TestCase):
    def setUp(self):
        # Crear usuario de prueba usando el modelo personalizado

        self.anonymous_user = Account.objects.create_user(
            first_name="Anónimo",
            last_name="Usuario",
            username="anonymus",
            email="anonymus@example.com",
            password="password",
        )

        self.user = Account.objects.create_user(
            first_name="Test",
            last_name="User",
            username="testuser",
            email="testuser@example.com",
            password="password",
        )

        # Crear productos de prueba
        self.category = Category.objects.create(
            category_name="Electrónica",
            description="Categoría de prueba para productos electrónicos",
            slug="electronica",
            cat_image="photos/categories/default.jpg"  # Puede ser un valor vacío o un mock
        )

        # Crear productos de prueba asociados a la categoría
        self.product1 = Product.objects.create(
            product_name="Producto 1",
            slug="producto-1",
            description="Primer producto de prueba",
            price=50,
            images="photos/products/producto1.jpg",
            stock=10,
            is_available=True,
            category=self.category  # Asociar a la categoría creada
        )
        self.product2 = Product.objects.create(
            product_name="Producto 2",
            slug="producto-2",
            description="Segundo producto de prueba",
            price=75,
            images="photos/products/producto2.jpg",
            stock=5,
            is_available=True,
            category=self.category
        )
        self.product3 = Product.objects.create(
            product_name="Producto 3",
            slug="producto-3",
            description="Tercer producto de prueba",
            price=100,
            images="photos/products/producto3.jpg",
            stock=2,
            is_available=True,
            category=self.category)


    def test_add_to_cart_anonymous(self):
        response = self.client.post(
            reverse('add_cart', args=[self.product1.id]), {'quantity': 1}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CartItem.objects.filter(product=self.product1).exists())

    def test_place_order_anonymous_less_than_three_products(self):
        self.client.post(reverse('add_cart', args=[self.product1.id]), {'quantity': 1})
        self.client.post(reverse('add_cart', args=[self.product2.id]), {'quantity': 1})

        # Datos necesarios para que el formulario sea válido
        order_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "email": "johndoe@example.com",
            "address_line_1": "123 Street",
            "address_line_2": "Apt 1",
            "country": "Country",
            "city": "City",
            "state": "State",
            "order_note": "Por favor, entregue en la puerta principal.",
        }

        response = self.client.post(reverse('place_order'), data=order_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.exists())

    def test_place_order_authenticated(self):
        self.client.login(username="testuser", password="password")

        self.client.post(reverse('add_cart', args=[self.product1.id]), {'quantity': 1})
        self.client.post(reverse('add_cart', args=[self.product2.id]), {'quantity': 1})

        order_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "email": "johndoe@example.com",
            "address_line_1": "123 Street",
            "address_line_2": "Apt 1",
            "country": "Country",
            "city": "City",
            "state": "State",
            "order_note": "Por favor, entregue en la puerta principal.",
        }

        response = self.client.post(reverse('place_order'), data=order_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.exists())

