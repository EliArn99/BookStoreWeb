import json

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CustomUserCreationForm, ProductForm, CustomerForm, OrderForm

from .models import Product, Customer, Order, OrderItem, ShippingAddress


class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(user=self.user, name="Test User", email="testuser@example.com")

        self.product = Product.objects.create(name="Test Product", price=10.00)

        self.order = Order.objects.create(customer=self.customer, complete=False)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_order_str(self):
        self.assertEqual(str(self.order), str(self.order.id))

    def test_order_get_cart_total(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        self.assertEqual(self.order.get_cart_total, 20.00)

    def test_order_get_cart_items(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        self.assertEqual(self.order.get_cart_items, 2)

    def test_customer_str(self):
        self.assertEqual(str(self.customer), "Test User")


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(user=self.user, name="Test User", email="testuser@example.com")
        self.client.login(username='testuser', password='testpassword')

        self.product = Product.objects.create(name="Test Product", price=10.00)
        self.order = Order.objects.create(customer=self.customer, complete=False)

    def test_store_view(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_cart_view(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        self.assertContains(response, "2")  # Quantity should be 2

    def test_checkout_view(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_user_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log In")


class TestForms(TestCase):
    def test_user_creation_form_invalid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password124',  # Mismatch in password
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_product_form_valid(self):
        form_data = {
            'name': 'New Product',
            'price': 20.00,
            'digital': False,
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_form_invalid(self):
        form_data = {
            'name': 'New Product',
            'price': -5.00,  # Invalid price
            'digital': False,
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_customer_form_valid(self):
        form_data = {
            'name': 'Test Customer',
            'email': 'testcustomer@example.com',
        }
        form = CustomerForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestOrderProcess(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.customer = Customer.objects.create(user=self.user)

        self.client.login(username='testuser', password='testpassword')

        self.product = Product.objects.create(name="Test Product", price=10.00)

        self.order = Order.objects.create(customer=self.customer, complete=False)

    def test_add_paroduct_to_cart(self):
        response = self.client.post(reverse('update_item'), json.dumps({
            'productId': self.product.id,
            'action': 'add'
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.order.get_cart_items, 1)

    def test_remove_product_from_cart(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1)
        response = self.client.post(reverse('update_item'), json.dumps({
            'productId': self.product.id,
            'action': 'remove'
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.order.get_cart_items, 0)

    def test_checkout_process(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
