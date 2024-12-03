from django.test import TestCase
from carts.models import Cart, CartItem
from store.models import Product, Variation
from accounts.models import Account
from category.models import Category


class CartModelTests(TestCase):
    def setUp(self):
        self.cart = Cart.objects.create(cart_id='12345ABC')

    def test_cart_creation(self):
        self.assertEqual(self.cart.cart_id, '12345ABC')
        self.assertEqual(str(self.cart), '12345ABC')


class CartItemModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name='Grandes electrodomésticos',
            slug='grandes-electrodomesticos'
        )

        self.user = Account.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            username='john',
            password='securepassword123'
        )

        self.product = Product.objects.create(
            product_name='Frigorífico',
            slug='frigorifico',
            description='Frigorífico de marca Samsung',
            price=200,
            stock=15,
            is_available=True,
            category=self.category
        )

        self.cart = Cart.objects.create(cart_id='67890DEF')

        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            cart=self.cart,
            quantity=2,
            is_active=True
        )

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertTrue(self.cart_item.is_active)

    def test_cart_item_sub_total(self):
        self.assertEqual(self.cart_item.sub_total(), 400)