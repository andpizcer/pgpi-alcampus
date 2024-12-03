from django.test import TestCase
from .models import Product, Category, Variation, ReviewRating
from accounts.models import Account

class ProductModelTests(TestCase):
    def setUp(self):
        # Crear categoría
        self.category = Category.objects.create(category_name='Electronics', slug='electronics')

        # Crear producto
        self.product = Product.objects.create(
            product_name='Laptop',
            slug='laptop',
            description='A high-end gaming laptop',
            price=1500,
            stock=10,
            is_available=True,
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.product_name, 'Laptop')
        self.assertEqual(self.product.category, self.category)
        self.assertTrue(self.product.is_available)

    def test_product_get_url(self):
        # Ajustar la URL esperada para que coincida con el formato actual
        self.assertEqual(self.product.get_url(), '/store/category/electronics/laptop/')


class VariationModelTests(TestCase):
    def setUp(self):
        # Crear categoría y producto
        self.category = Category.objects.create(category_name='Clothing', slug='clothing')
        self.product = Product.objects.create(
            product_name='T-Shirt',
            slug='t-shirt',
            description='A comfortable cotton t-shirt',
            price=20,
            stock=50,
            is_available=True,
            category=self.category
        )

        # Crear variaciones
        self.color_variation = Variation.objects.create(
            product=self.product,
            variation_category='color',
            variation_value='Blue',
            is_active=True
        )
        self.size_variation = Variation.objects.create(
            product=self.product,
            variation_category='talla',
            variation_value='M',
            is_active=True
        )

    def test_variation_creation(self):
        self.assertEqual(self.color_variation.variation_value, 'Blue')
        self.assertEqual(self.size_variation.variation_value, 'M')
        self.assertTrue(self.color_variation.is_active)


class ReviewRatingModelTests(TestCase):
    def setUp(self):
        # Crear usuario, categoría y producto
        self.user = Account.objects.create_user(
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            username='jane',
            password='securepassword123'
        )
        self.category = Category.objects.create(category_name='Books', slug='books')
        self.product = Product.objects.create(
            product_name='Fiction Novel',
            slug='fiction-novel',
            description='A thrilling fiction novel.',
            price=15,
            stock=20,
            is_available=True,
            category=self.category
        )

        # Crear review
        self.review = ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            subject='Great Book!',
            review='I really enjoyed this novel.',
            rating=4.5,
            ip='127.0.0.1',
            status=True
        )

    def test_review_creation(self):
        self.assertEqual(self.review.subject, 'Great Book!')
        self.assertEqual(self.review.rating, 4.5)
        self.assertTrue(self.review.status)
