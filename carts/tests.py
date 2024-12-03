from django.test import TestCase
from carts.models import Cart, CartItem
from store.models import Product, Variation
from accounts.models import Account
from category.models import Category


class CartModelTests(TestCase):
    def setUp(self):
        # Crear carrito
        self.cart = Cart.objects.create(cart_id='12345ABC')

    def test_cart_creation(self):
        self.assertEqual(self.cart.cart_id, '12345ABC')
        self.assertEqual(str(self.cart), '12345ABC')


class CartItemModelTests(TestCase):
    def setUp(self):
        # Crear categoría para el producto
        self.category = Category.objects.create(
            category_name='Electronics',
            slug='electronics'
        )

        # Crear usuario
        self.user = Account.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            username='john',
            password='securepassword123'
        )

        # Crear producto
        self.product = Product.objects.create(
            product_name='Headphones',
            slug='headphones',
            description='Noise-canceling headphones',
            price=200,
            stock=15,
            is_available=True,
            category=self.category
        )

        # Crear variación del producto
        self.variation = Variation.objects.create(
            product=self.product,
            variation_category='color',
            variation_value='Black',
            is_active=True
        )

        # Crear carrito
        self.cart = Cart.objects.create(cart_id='67890DEF')

        # Crear item del carrito
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            cart=self.cart,
            quantity=2,
            is_active=True
        )
        self.cart_item.variation.add(self.variation)

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertTrue(self.cart_item.is_active)

    def test_cart_item_sub_total(self):
        self.assertEqual(self.cart_item.sub_total(), 400)

    def test_cart_item_variation(self):
        self.assertIn(self.variation, self.cart_item.variation.all())