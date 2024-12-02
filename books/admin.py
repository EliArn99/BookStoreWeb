from django.contrib import admin
from .models import Product, Order, Customer, OrderItem, ShippingAddress, BlogPost

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'digital')  # Display these fields in the admin list
    list_filter = ('digital',)  # Add a filter for 'digital' field
    search_fields = ('name',)  # Add search functionality for 'name'
    ordering = ('price',)  # Default ordering by price

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'complete', 'transaction_id', 'date_ordered')  # Display these fields
    list_filter = ('complete', 'date_ordered')  # Filter by completion status and date
    search_fields = ('transaction_id',)  # Add search functionality for transaction_id
    ordering = ('-date_ordered',)  # Default ordering by most recent orders

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user')  # Show name, email, and associated user
    search_fields = ('name', 'email')  # Add search by name and email
    ordering = ('name',)  # Default ordering alphabetically by name

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added')  # Show relevant fields
    list_filter = ('date_added',)  # Filter by date added
    ordering = ('-date_added',)  # Order by most recent additions

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'address', 'city', 'state', 'zipcode', 'date_added')
    list_filter = ('city', 'state')  # Filter by city and state
    search_fields = ('address', 'city', 'state', 'zipcode')  # Add search
    ordering = ('-date_added',)  # Default ordering by most recent

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')  # Show title, author, and timestamps
    search_fields = ('title', 'content')  # Allow search by title or content
    list_filter = ('author', 'created_at')  # Filter by author and creation date
    ordering = ('-created_at',)  # Order by most recent posts
