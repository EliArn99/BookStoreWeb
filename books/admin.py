from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Customer, Book, Order, OrderItem, ShippingAddress, Category, Review, Post, Banner


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price', 'stock', 'category', 'is_digital', 'image_tag')

    list_editable = ('price', 'stock')

    list_filter = ('category', 'digital', 'stock')
    search_fields = ('name', 'author', 'description')

    def image_tag(self, obj):
        if obj.image:
            return mark_safe('<img src="%s" width="50" height="75" style="object-fit: cover;" />' % obj.image.url)
        return "Няма снимка"

    image_tag.short_description = 'Снимка'

    def is_digital(self, obj):
        return "Да" if obj.digital else "Не"

    is_digital.short_description = 'Дигитална'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['product_name', 'product_price']

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = 'Продукт'

    def product_price(self, obj):
        return f"{obj.product.price} лв."

    product_price.short_description = 'Цена'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered', 'complete', 'get_cart_total', 'transaction_id')
    list_filter = ('complete', 'date_ordered')
    search_fields = ('customer__name', 'transaction_id')
    inlines = [OrderItemInline]
    readonly_fields = ('get_cart_total',)

    def get_cart_total(self, obj):
        return f"{obj.get_cart_total} лв."

    get_cart_total.short_description = 'Обща сума'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at', 'comment')
    list_filter = ('rating', 'book')
    search_fields = ('book__name', 'user__username', 'comment')
    readonly_fields = ('created_at',)
    list_per_page = 20


admin.site.register(Customer)
admin.site.register(ShippingAddress)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title',)
