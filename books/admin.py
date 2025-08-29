from django.contrib import admin
from .models import Product, Order, Customer, OrderItem, ShippingAddress, BlogPost


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'digital')
    list_filter = ('digital',)
    search_fields = ('name',)
    ordering = ('price',)
