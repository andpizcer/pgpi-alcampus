from django.test import TestCase
from store.models import Product, Variation, ReviewRating, ProductGallery
from category.models import Category
from accounts.models import Account

class ProductModelTests(TestCase):
    def setUp(self):
        # Crear categoría
        self.category = Category.objects.create(name='Electronics', slug='electronics')

        # Crear producto
        self.product = Product.objects.create(
            product_name='Laptop',
            slug='laptop',
            description='High-end gaming laptop',
            price=1500,
            stock=10,
            is_available=True,
            category=self.category
        )

        # Crear usuario
        self.user = Account.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            username='john',
            password='securepassword123'
        )

        # Crear reseñas
        ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            subject='Great product',
            review='Loved the performance!',
            rating=5.0,
            status=True
        )
        ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            subject='Not bad',
            review='Good value for money.',
            rating=4.0,
            status=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.product_name, 'Laptop')
        self.assertTrue(self.product.is_available)
        self.assertEqual(self.product.category, self.category)

    def test_product_url(self):
        url = self.product.get_url()
        expected_url = f'/store/{self.category.slug}/{self.product.slug}/'
        self.assertEqual(url, expected_url)

    def test_average_review(self):
        avg_rating = self.product.averageReview()
        self.assertEqual(avg_rating, 4.5)  # (5.0 + 4.0) / 2

    def test_count_review(self):
        review_count = self.product.countReview()
        self.assertEqual(review_count, 2)

class VariationModelTests(TestCase):
    def setUp(self):
        # Crear producto
        self.product = Product.objects.create(
            product_name='Laptop',
            slug='laptop',
            description='High-end gaming laptop',
            price=1500,
            stock=10,
            is_available=True,
            category=Category.objects.create(name='Electronics', slug='electronics')
        )

        # Crear variaciones
        self.color = Variation.objects.create(
            product=self.product,
            variation_category='color',
            variation_value='Black',
            is_active=True
        )
        self.talla = Variation.objects.create(
            product=self.product,
            variation_category='talla',
            variation_value='Large',
            is_active=True
        )

    def test_variation_creation(self):
        self.assertEqual(self.color.variation_category, 'color')
        self.assertEqual(self.color.variation_value, 'Black')
        self.assertTrue(self.color.is_active)

    def test_variation_manager_colors(self):
        colors = Variation.objects.colors()
        self.assertIn(self.color, colors)
        self.assertNotIn(self.talla, colors)

    def test_variation_manager_tallas(self):
        tallas = Variation.objects.tallas()
        self.assertIn(self.talla, tallas)
        self.assertNotIn(self.color, tallas)

class ProductGalleryTests(TestCase):
    def setUp(self):
        # Crear producto
        self.product = Product.objects.create(
            product_name='Smartphone',
            slug='smartphone',
            description='Latest model smartphone',
            price=800,
            stock=20,
            is_available=True,
            category=Category.objects.create(name='Electronics', slug='electronics')
        )

        # Crear imágenes de la galería
        self.gallery_item = ProductGallery.objects.create(
            product=self.product,
            image='store/products/smartphone1.jpg'
        )

    def test_product_gallery_creation(self):
        self.assertEqual(self.gallery_item.product, self.product)
        self.assertEqual(self.gallery_item.image, 'store/products/smartphone1.jpg')
