from django.test import TestCase
from .models import Product, Category, Variation, ReviewRating
from accounts.models import Account

class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name='Grandes electrodomésticos', slug='grandes-electrodomesticos')

        self.product = Product.objects.create(
            product_name='Frigorífico',
            slug='frigorifico',
            description='Frigorífico de marca Samsung',
            price=1500,
            stock=10,
            is_available=True,
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.product_name, 'Frigorífico')
        self.assertEqual(self.product.category, self.category)
        self.assertTrue(self.product.is_available)

    def test_product_get_url(self):
        self.assertEqual(self.product.get_url(), '/store/category/grandes-electrodomesticos/frigorifico/')
