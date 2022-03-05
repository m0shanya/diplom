from django.contrib import admin

from shop.models import Product, Buy


class PurchaseInline(admin.TabularInline):
    model = Buy


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "cost")
    search_fields = ("title",)
    inlines = [
        PurchaseInline,
    ]
