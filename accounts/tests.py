from django.test import TestCase
from django.urls import reverse
from .models import Account

class AccountViewTests(TestCase):
    def setUp(self):
        self.valid_user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123'
        }

        self.login_data = {
            'email': 'john@example.com',
            'password': 'securepassword123'
        }

    def test_register_user_success(self):
        response = self.client.post(reverse('register'), self.valid_user_data)
        self.assertEqual(response.status_code, 302)  # Redirige tras registro
        self.assertTrue(Account.objects.filter(email='john@example.com').exists())
        user = Account.objects.get(email='john@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.is_active, False)  # La cuenta no está activa aún

    def test_register_user_missing_field(self):
        invalid_user_data = self.valid_user_data.copy()
        invalid_user_data.pop('email')  # Quitamos el email
        response = self.client.post(reverse('register'), invalid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Account.objects.filter(first_name='John').exists())

    def test_login_success(self):
        user = Account.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            username='john',
            password='securepassword123'
        )
        user.is_active = True
        user.save()

        response = self.client.post(reverse('login'), self.login_data)
        self.assertEqual(response.status_code, 302) 
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_failed_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'email': 'john@example.com', 'password': 'wrongpassword'})
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse('_auth_user_id' in self.client.session)
