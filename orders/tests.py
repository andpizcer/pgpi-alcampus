from django.test import TestCase
from django.contrib.auth import get_user_model
from category.models import Category
from store.models import Product, Variation, ReviewRating, ProductGallery   
from orders.models import Order, OrderProduct, Payment
from accounts.models import Account


class OrderModelTest(TestCase):
    
    def setUp(self):
        # Crear un usuario de prueba
        self.user = get_user_model().objects.create_user(
            first_name="John", 
            last_name="Doe", 
            email="john.doe@example.com", 
            username="johndoe", 
            password="password123"
        )

        # Crear una categoría de prueba
        self.category = Category.objects.create(
            category_name="Electronics", 
            slug="electronics"
        )

        # Crear un producto de prueba
        self.product = Product.objects.create(
            product_name="Smartphone", 
            slug="smartphone", 
            description="A great smartphone", 
            price=200, 
            stock=50, 
            is_available=True, 
            category=self.category
        )

        # Crear una variación de producto
        self.variation = Variation.objects.create(
            product=self.product, 
            variation_category="color", 
            variation_value="red"
        )

        # Crear un pedido de prueba
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

        # Crear un pago de prueba
        self.payment = Payment.objects.create(
            user=self.user,
            payment_id="PAY12345",
            payment_method="Credit Card",
            amount_id="AMT12345",
            status="Completed"
        )

        # Crear un producto en el pedido
        self.order_product = OrderProduct.objects.create(
            order=self.order,
            user=self.user,
            product=self.product,
            quantity=1,
            product_price=self.product.price
        )
    
    def test_product_review_count(self):
        # Crear una reseña para el producto
        ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            rating=4.5,
            subject="Great product",
            review="I really loved this smartphone",
            status=True
        )

        # Verificar que el conteo de reseñas del producto sea correcto
        self.assertEqual(self.product.countReview(), 1)

    def test_product_average_rating(self):
        # Crear reseñas para el producto
        ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            rating=4.0,
            subject="Good product",
            review="The product is good, but could be improved.",
            status=True
        )

        ReviewRating.objects.create(
            product=self.product,
            user=self.user,
            rating=5.0,
            subject="Excellent product",
            review="The product is amazing.",
            status=True
        )

        # Verificar que la calificación promedio del producto sea correcta
        self.assertEqual(self.product.averageReview(), 4.5)

    def test_product_gallery_creation(self):
        # Crear una galería de productos
        product_gallery = ProductGallery.objects.create(
            product=self.product,
            image="photos/products/smartphone_image.jpg"
        )

        # Verificar que la galería esté asociada correctamente al producto
        self.assertEqual(product_gallery.product, self.product)

    def test_order_creation(self):
        # Verificar que el pedido se cree correctamente
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.order_number, "ORD12345")
        self.assertEqual(self.order.status, "New")
    
    def test_order_product_creation(self):
        # Verificar que el producto esté en el pedido correctamente
        self.assertEqual(self.order_product.product, self.product)
        self.assertEqual(self.order_product.quantity, 1)
        self.assertEqual(self.order_product.product_price, self.product.price)
