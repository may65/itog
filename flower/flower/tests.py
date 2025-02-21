# flower/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem
from django.urls import reverse
import datetime


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name='Роза', price=10.99)

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Роза')
        self.assertEqual(self.product.price, 10.99)

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            delivery_address='ул. Тестовая, 1',
            delivery_time=datetime.datetime.now(),
            customer_phone='+79990000000'
        )
        OrderItem.objects.create(order=order, product=self.product, quantity=2)

        self.assertEqual(order.orderitem_set.count(), 1)
        self.assertEqual(order.orderitem_set.first().quantity, 2)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name='Тюльпан', price=5.99)

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тюльпан')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('view_cart'))

        session = self.client.session
        self.assertEqual(session['cart'][str(self.product.id)], 1)

    def test_order_creation_flow(self):
        self.client.login(username='testuser', password='12345')

        # Добавляем товар в корзину
        self.client.post(reverse('add_to_cart', args=[self.product.id]))

        # Оформляем заказ
        response = self.client.post(reverse('create_order'), {
            'delivery_address': 'ул. Тестовая, 2',
            'delivery_time': '2023-12-31 12:00',
            'customer_phone': '+79991112233'
        })

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Заказ #1')


class AuthTests(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse('home'))

    def test_login_logout(self):
        User.objects.create_user(username='testuser', password='12345')

        # Тест входа
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertRedirects(response, reverse('home'))

        # Тест выхода
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))