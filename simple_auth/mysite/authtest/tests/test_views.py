from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate, login

from ..forms import RegisterForm, AuthorizeForm

from unittest import skip


# Тесты для страницы регистрации
class RegisterPageTestCase(TestCase):
    def test_correct_html_template_on_register_uri(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'authtest/register.html')

    def test_correct_form_on_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertIsInstance(response.context['form'], RegisterForm)


# Тесты для страницы авторизации
class AuthorizePageTestCase(TestCase):
    def test_correct_html_template_on_register_uri(self):
        response = self.client.get(reverse('authorize'))
        self.assertTemplateUsed(response, 'authtest/authorize.html')

    def test_correct_form_on_authorize_page(self):
        response = self.client.get(reverse('authorize'))
        self.assertIsInstance(response.context['form'], AuthorizeForm)

