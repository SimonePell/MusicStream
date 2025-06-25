from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsTests(TestCase):
    def test_register_page_status(self):
        resp = self.client.get(reverse('accounts:register'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<form')

    def test_user_registration_and_login(self):
        # Registrazione
        data = {
            'username': 'provatester',
            'email': 't@e.com',
            'password1': 'ComplexPwd123',
            'password2': 'ComplexPwd123',
        }
        resp = self.client.post(reverse('accounts:register'), data)
        self.assertRedirects(resp, reverse('accounts:login'))

        # Login
        login_ok = self.client.login(username='provatester', password='ComplexPwd123')
        self.assertTrue(login_ok)

        # Profilo
        resp = self.client.get(reverse('accounts:profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Profilo di provatester')
