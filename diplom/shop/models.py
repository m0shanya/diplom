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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="Заказы")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    purchase = models.ForeignKey(
        Product, related_name="purchases", on_delete=models.CASCADE, null=True,
    )
    count = models.IntegerField(null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=250, default=0)
    address = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Order'
        verbose_name_plural = 'Order'

    def __str__(self):
        return f"Order №{self.id}"

    def get_cost(self):
        return self.cost * self.count


class Category(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_list_by_category',
                        args=[self.slug])


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"Comment by {self.name} on {self.product}"
