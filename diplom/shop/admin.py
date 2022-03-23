from django.contrib import admin

from shop.models import Product, Buy, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class CategoryAdminInline(admin.TabularInline):
    model = Category


class PurchaseInline(admin.TabularInline):
    model = Buy


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "cost", "category")
    search_fields = ("title",)
    inlines = [
        PurchaseInline,
    ]
