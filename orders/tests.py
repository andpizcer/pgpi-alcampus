from django.test import TestCase
from django.contrib.auth import get_user_model
from category.models import Category
from store.models import Product, Variation, ReviewRating, ProductGallery   
from orders.models import Order, OrderProduct, Payment
from accounts.models import Account


class OrderModelTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name="John", 
            last_name="Doe", 
            email="john.doe@example.com", 
            username="johndoe", 
            password="password123"
        )

        self.category = Category.objects.create(
            category_name="Grandes electrodomésticos", 
            slug="grandes-electrodomesticos"
        )

        self.product = Product.objects.create(
            product_name="Frigorífico", 
            slug="frigorifico", 
            description="Frigorífico de marca Samsung", 
            price=200, 
            stock=50, 
            is_available=True, 
            category=self.category
        )

        self.order = Order.objects.create(
            user=self.user,
            order_number="ORD12345",
            first_name="John",
            last_name="Doe",
            phone="123456789",
            email="john.doe@example.com",
            address_line_1="123 Main St",
            address_line_2="Apt 4B",
            country="USA",
            city="New York",
            state="NY",
            order_total=200,
            tax=20,
            status="New",
            ip="127.0.0.1",
            is_ordered=False
        )

        self.payment = Payment.objects.create(
            user=self.user,
            payment_id="PAY12345",
            payment_method="Credit Card",
            amount_id="AMT12345",
            status="Completed"
        )

        self.order_product = OrderProduct.objects.create(
            order=self.order,
            user=self.user,
            product=self.product,
            quantity=1,
            product_price=self.product.price
        )

    def test_product_gallery_creation(self):
        product_gallery = ProductGallery.objects.create(
            product=self.product,
            image="media/photos/frigorifico.jpg"
        )
        self.assertEqual(product_gallery.product, self.product)

    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.order_number, "ORD12345")
        self.assertEqual(self.order.status, "New")
    
    def test_order_product_creation(self):
        self.assertEqual(self.order_product.product, self.product)
        self.assertEqual(self.order_product.quantity, 1)
        self.assertEqual(self.order_product.product_price, self.product.price)
