from django.contrib import admin
from .models import Product, Order, Customer, OrderItem, ShippingAddress, BlogPost


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'digital')
    list_filter = ('digital',)
    search_fields = ('name',)
    ordering = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'complete', 'transaction_id', 'date_ordered')
    list_filter = ('complete', 'date_ordered')
    search_fields = ('transaction_id',)
    ordering = ('-date_ordered',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user')
    search_fields = ('name', 'email')
    ordering = ('name',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added')
    list_filter = ('date_added',)
    ordering = ('-date_added',)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'address', 'city', 'state', 'zipcode', 'date_added')
    list_filter = ('city', 'state')
    search_fields = ('address', 'city', 'state', 'zipcode')
    ordering = ('-date_added',)


# Customizing BlogPost Admin


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('author', 'created_at')
    ordering = ('-created_at',)
