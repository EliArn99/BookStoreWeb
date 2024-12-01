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
    def test_user_creation_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = CustomUserCreationForm(data=form_data)
        print(form.errors)  # Print form errors for debugging

        # Also print cleaned data to ensure it's being populated correctly
        print(form.cleaned_data)  # Debugging: see cleaned data

        # Assert that the form is valid
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

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

    def test_process_order(self):
        # Create an order item to ensure the cart has items
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1)

        # Ensure the total calculated by the order matches the expected value
        expected_total = self.order.get_cart_total

        # Now, let's post the request to the `process_order` endpoint
        response = self.client.post(reverse('process_order'), json.dumps({
            'form': {'total': expected_total},  # Send the correct total
            'shipping': {
                'address': '123 Main St',
                'city': 'Springfield',
                'state': 'IL',
                'zipcode': '62701',
            }
        }), content_type="application/json")

        # Check that the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the order is marked as complete
        self.order.refresh_from_db()  # Refresh the order from the database to get the latest state
        self.assertTrue(self.order.complete)

        # Optional: You can check that a shipping address was created
        self.assertEqual(ShippingAddress.objects.count(), 1)

    def test_checkout_process(self):
        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

# from django.db import IntegrityError
# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .models import BlogPost, Product, Order, Customer, OrderItem
# from .forms import BlogPostForm, CustomUserCreationForm, OrderForm
# from django.contrib.auth import get_user_model
#
#
# class TestModels(TestCase):
#
#     def test_order_invalid_data(self):
#         # Create a customer and order
#         customer = Customer.objects.create(user=User.objects.create_user('testuser'))
#         order = Order.objects.create(customer=customer, complete=False)
#
#         # Expecting an error when trying to create OrderItem with invalid product (None)
#         with self.assertRaises(IntegrityError):  # We expect IntegrityError here
#             OrderItem.objects.create(order=order, product=None, quantity=2)
#
#     def test_order_cart_total_with_no_items(self):
#         customer = Customer.objects.create(user=User.objects.create_user('testuser'))
#         order = Order.objects.create(customer=customer, complete=False)
#         self.assertEqual(order.get_cart_total, 0.0)  # No items in the cart, total should be 0.
#
#     def test_order_cart_items_with_no_items(self):
#         customer = Customer.objects.create(user=User.objects.create_user('testuser'))
#         order = Order.objects.create(customer=customer, complete=False)
#         self.assertEqual(order.get_cart_items, 0)  # No items in the cart, item count should be 0.
#
#     def test_order_without_customer(self):
#         # Test creating an order without a linked customer.
#         product = Product.objects.create(name="Test Product", price=10.0)
#         order = Order.objects.create(complete=False)
#         OrderItem.objects.create(order=order, product=product, quantity=2)
#         self.assertEqual(order.get_cart_total, 20.0)  # Should still calculate total, but this may raise an exception depending on model logic.
#
#     def test_order_without_product(self):
#         customer = Customer.objects.create(user=User.objects.create_user('testuser'))
#         order = Order.objects.create(customer=customer, complete=False)
#         self.assertEqual(order.get_cart_total, 0.0)  # No items in the order.
#
#     def test_order_invalid_data(self):
#         customer = Customer.objects.create(user=User.objects.create_user('testuser'))
#         order = Order.objects.create(customer=customer, complete=False)
#         with self.assertRaises(ValueError):
#             # Trying to add an invalid product or data
#             OrderItem.objects.create(order=order, product=None, quantity=2)
#
#
# class TestForms(TestCase):
#
#     def test_custom_user_creation_form_valid(self):
#         form_data = {
#             'username': 'testuser',
#             'email': 'test@example.com',
#             'password1': 'StrongPassword123',
#             'password2': 'StrongPassword123',
#         }
#         form = CustomUserCreationForm(data=form_data)
#         self.assertTrue(form.is_valid())
#
#     def test_custom_user_creation_form_invalid(self):
#         form_data = {
#             'username': 'testuser',
#             'email': 'test@example.com',
#             'password1': 'password',
#             'password2': 'password',
#         }
#         form = CustomUserCreationForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertEqual(len(form.errors), 1)  # The password is weak.
#
#     def test_blog_post_form_valid(self):
#         user = User.objects.create_user(username="author", password="password")
#         form_data = {
#             'title': 'Test Blog Post',
#             'content': 'This is a test blog post.',
#             'author': user.id,
#         }
#         form = BlogPostForm(data=form_data)
#         self.assertTrue(form.is_valid())
#
#     def test_blog_post_form_invalid(self):
#         form_data = {
#             'title': '',
#             'content': 'This is a test blog post.',
#         }
#         form = BlogPostForm(data=form_data)
#         self.assertFalse(form.is_valid())
#         self.assertEqual(len(form.errors), 1)
#
#
# class TestViews(TestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='password')
#         # Create a customer for the user
#         self.customer = Customer.objects.create(user=self.user, name="John Doe", email="john@example.com")
#         self.blog_post = BlogPost.objects.create(
#             title='Test Post',
#             content='Test content',
#             author=self.user
#         )
#
#     def test_blog_post_create_view_authenticated(self):
#         self.client.login(username='testuser', password='password')
#         response = self.client.get(reverse('blog-create'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'books/blog_form.html')  # Update the template name here
#
#     def test_blog_post_create_view_not_authenticated(self):
#         response = self.client.get(reverse('blog-create'))
#         self.assertRedirects(response, '/accounts/login/?next=/blog/create/')  # Ensure redirection for unauthenticated users.
#
#     def test_manage_order_view_post_authenticated(self):
#         order = Order.objects.create(customer=self.customer, complete=False)
#         response = self.client.post(reverse('manage-order', kwargs={'pk': order.id}), {
#             'customer': self.customer.id,
#             'complete': True,
#             'transaction_id': '12345'
#         })
#         self.assertEqual(response.status_code, 302)  # Should redirect after the order is updated.
#
#     def test_manage_order_view_post_unauthenticated(self):
#         order = Order.objects.create(customer=self.customer, complete=False)
#         response = self.client.post(reverse('manage-order', kwargs={'pk': order.id}), {
#             'customer': self.customer.id,
#             'complete': True,
#             'transaction_id': '12345'
#         })
#         self.assertRedirects(response, '/accounts/login/?next=/order/manage/{}/'.format(order.id))  # Redirect if not logged in.
#
#     def test_manage_order_view_post_no_permissions(self):
#         # Create a second user without permissions to manage orders
#         another_user = User.objects.create_user(username='anotheruser', password='password')
#         self.client.login(username='anotheruser', password='password')
#         order = Order.objects.create(customer=self.customer, complete=False)
#
#         response = self.client.post(reverse('manage-order', kwargs={'pk': order.id}), {
#             'customer': self.customer.id,
#             'complete': True,
#             'transaction_id': '12345'
#         })
#         self.assertEqual(response.status_code, 403)
#
#     def test_cart_view_authenticated(self):
#         self.client.login(username='testuser', password='password')
#         response = self.client.get(reverse('cart'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'books/cart.html')
#
#     def test_cart_view_not_authenticated(self):
#         response = self.client.get(reverse('cart'))
#         self.assertRedirects(response, '/accounts/login/?next=/cart/')  # Should redirect if the user is not authenticated.
#
#     def test_checkout_view_authenticated(self):
#         self.client.login(username='testuser', password='password')
#         response = self.client.get(reverse('checkout'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'books/checkout.html')
#
#     def test_checkout_view_not_authenticated(self):
#         response = self.client.get(reverse('checkout'))
#         self.assertRedirects(response, '/accounts/login/?next=/checkout/')
