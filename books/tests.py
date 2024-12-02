import json

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .forms import CustomUserCreationForm, ProductForm, CustomerForm, OrderForm

from .models import Product, Customer, Order, OrderItem, ShippingAddress


class TestModels(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(user=self.user, name="Test User", email="testuser@example.com")

        # Create a test product
        self.product = Product.objects.create(name="Test Product", price=10.00)

        # Create an order for the customer
        self.order = Order.objects.create(customer=self.customer, complete=False)

    def test_product_str(self):
        # Test the __str__ method of the Product model
        self.assertEqual(str(self.product), "Test Product")

    def test_order_str(self):
        # Test the __str__ method of the Order model
        self.assertEqual(str(self.order), str(self.order.id))

    def test_order_get_cart_total(self):
        # Test the get_cart_total method
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        self.assertEqual(self.order.get_cart_total, 20.00)

    def test_order_get_cart_items(self):
        # Test the get_cart_items method
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        self.assertEqual(self.order.get_cart_items, 2)

    def test_customer_str(self):
        # Test the __str__ method of the Customer model
        self.assertEqual(str(self.customer), "Test User")


class TestViews(TestCase):

    def setUp(self):
        # Create a test user and customer
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(user=self.user, name="Test User", email="testuser@example.com")
        self.client.login(username='testuser', password='testpassword')

        # Create a product and order for the customer
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

    def test_order_form_valid(self):
        customer = Customer.objects.create(name="Test User", email="testuser@example.com")
        form_data = {
            'customer': customer.id,
            'complete': False,
            'transaction_id': '123abc',
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestOrderProcess(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a customer for the user (assuming the Customer model has a OneToOne relationship with User)
        self.customer = Customer.objects.create(user=self.user)

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create a product
        self.product = Product.objects.create(name="Test Product", price=10.00)

        # Create an order for the customer
        self.order = Order.objects.create(customer=self.customer, complete=False)

    def test_add_product_to_cart(self):
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
