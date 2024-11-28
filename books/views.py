from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from BookWeb_demo.books.models import Product, OrderItem, ShippingAddress, Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, BlogPostForm, CustomerForm, OrderForm, ProductForm
import json
import datetime
from django.shortcuts import render
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import BlogPost


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES.get('cart', '{}'))
        except json.JSONDecodeError:
            cart = {}

        cartItems = sum(item['quantity'] for item in cart.values())

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems
    }
    return render(request, 'books/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES.get('cart', '{}'))  # Retrieve cart from cookies
        except json.JSONDecodeError:
            cart = {}

        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = 0

        for productId, details in cart.items():
            try:
                product = Product.objects.get(id=productId)
                total = product.price * details['quantity']

                cartItems += details['quantity']

                items.append({
                    'product': product,
                    'quantity': details['quantity'],
                    'get_total': total
                })

                order['get_cart_total'] += total
                order['get_cart_items'] = cartItems
            except Product.DoesNotExist:
                continue

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'books/cart.html', context)


@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'books/checkout.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'books/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'books/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print("User in not logged in..")
    return JsonResponse('Payment compete!', safe=False)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'books/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.customer


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'books/blog_list.html'
    context_object_name = 'posts'


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'books/blog_detail.html'


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'books/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'books/blog_form.html'

    def test_func(self):
        blog_post = self.get_object()  # Fetch the blog post being edited
        return self.request.user == blog_post.author  # Only allow the author to edit


class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'books/blog_confirm_delete.html'
    success_url = '/blogs/'  # Redirect to the blog list after deletion

    def test_func(self):
        blog_post = self.get_object()  # Fetch the blog post being deleted
        return self.request.user == blog_post.author  # Only allow the author to delete


def manage_order(request, pk=None):
    if pk:
        order = get_object_or_404(Order, pk=pk)
        form = OrderForm(instance=order)
    else:
        form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order if pk else None)
        if form.is_valid():
            form.save()
            return redirect('store')  # Redirect to a relevant page

    return render(request, 'books/manage_order.html', {'form': form})


def manage_product(request, pk=None):
    if pk:
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
    else:
        form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product if pk else None)
        if form.is_valid():
            form.save()
            return redirect('store')

    return render(request, 'books/manage_product.html', {'form': form})


def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('profile-detail')

    return render(request, 'books/update_customer.html', {'form': form})
