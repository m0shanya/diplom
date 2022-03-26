from django.conf import settings
from django.db import models
from django.urls import reverse
from .validators import image_resolution_check_big


class Product(models.Model):
    image = models.ImageField(validators=[image_resolution_check_big], null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    slug = models.SlugField(max_length=200)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE
    )
    cost = models.DecimalField(decimal_places=2, max_digits=250, default=0)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return f"{self.title} - {self.cost}"


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class Buy(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    purchase = models.ForeignKey(
        Product, related_name="purchases", on_delete=models.CASCADE
    )
    count = models.IntegerField()
    cost = models.DecimalField(decimal_places=2, max_digits=250, default=0)

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.cost * self.count


class Category(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_list_by_category',
                        args=[self.slug])
