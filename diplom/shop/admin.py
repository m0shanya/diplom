from django.contrib import admin

from shop.models import Product, Category, Order, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class CategoryAdminInline(admin.TabularInline):
    model = Category


class PurchaseInline(admin.TabularInline):
    model = Order
    raw_id_fields = ['purchase']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "cost", "category")
    search_fields = ("title",)
    inlines = [
        PurchaseInline,
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'paid',
                    'created_at', 'updated']
    list_filter = ['paid', 'created_at', 'updated']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'product', 'created_at', 'active')
    list_filter = ('active', 'created_at', 'updated')
    search_fields = ('name', 'email', 'body')
