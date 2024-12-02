from django.test import TestCase
from accounts.models import Account
from store.models import Product, Variation
from orders.models import Payment, Order, OrderProduct


class PaymentModelTests(TestCase):
    def setUp(self):
        # Crear usuario
        self.user = Account.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            username='john',
            password='securepassword123'
        )

        # Crear pago
        self.payment = Payment.objects.create(
            user=self.user,
            payment_id='PAY12345',
            payment_method='Credit Card',
            amount_id='100.00',
            status='Completed'
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.payment_id, 'PAY12345')
        self.assertEqual(self.payment.payment_method, 'Credit Card')
        self.assertEqual(self.payment.status, 'Completed')
        self.assertEqual(str(self.payment), 'PAY12345')


class OrderModelTests(TestCase):
    def setUp(self):
        # Crear usuario
        self.user = Account.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            username='john',
            password='securepassword123'
        )

        # Crear pago
        self.payment = Payment.objects.create(
            user=self.user,
            payment_id='PAY12345',
            payment_method='Credit Card',
            amount_id='100.00',
            status='Completed'
        )

        # Crear orden
        self.order = Order.objects.create(
            user=self.user,
            payment=self.payment,
            order_number='ORD12345',
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            email='john@example.com',
            address_line_1='123 Main St',
            address_line_2='Apt 4B',
            country='USA',
            city='New York',
            state='10001',
            order_total=150.0,
            tax=10.0,
            status='New',
            is_ordered=True
        )

    def test_order_creation(self):
        self.assertEqual(self.order.order_number, 'ORD12345')
        self.assertTrue(self.order.is_ordered)
        self.assertEqual(self.order.status, 'New')

    def test_order_full_name(self):
        self.assertEqual(self.order.full_name(), 'John Doe')

    def test_order_full_address(self):
        self.assertEqual(self.order.full_address(), '123 Main St Apt 4B')

    def test_order_relationships(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.payment, self.payment)


class OrderProductModelTests(TestCase):
    def setUp(self):
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
            product_name='Laptop',
            slug='laptop',
            description='Gaming laptop',
            price=1500,
            stock=5,
            is_available=True,
            category=None
        )

        # Crear pago
        self.payment = Payment.objects.create(
            user=self.user,
            payment_id='PAY12345',
            payment_method='Credit Card',
            amount_id='100.00',
            status='Completed'
        )

        # Crear orden
        self.order = Order.objects.create(
            user=self.user,
            payment=self.payment,
            order_number='ORD12345',
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            email='john@example.com',
            address_line_1='123 Main St',
            address_line_2='Apt 4B',
            country='USA',
            city='New York',
            state='10001',
            order_total=150.0,
            tax=10.0,
            status='New',
            is_ordered=True
        )

        # Crear producto de orden
        self.order_product = OrderProduct.objects.create(
            order=self.order,
            payment=self.payment,
            user=self.user,
            product=self.product,
            quantity=1,
            product_price=self.product.price,
            ordered=True
        )

    def test_order_product_creation(self):
        self.assertEqual(self.order_product.product, self.product)
        self.assertEqual(self.order_product.quantity, 1)
        self.assertEqual(self.order_product.product_price, 1500.0)
        self.assertTrue(self.order_product.ordered)

    def test_order_product_relationships(self):
        self.assertEqual(self.order_product.order, self.order)
        self.assertEqual(self.order_product.payment, self.payment)
        self.assertEqual(self.order_product.user, self.user)

    def test_order_product_string_representation(self):
        self.assertEqual(str(self.order_product), 'Laptop')
