from django.conf import settings
from django.db import models
from django.urls import reverse


class Product(models.Model):
    image = models.ImageField(null=True, blank=True)
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



class Buy(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="purchases", on_delete=models.CASCADE
    )
    purchase = models.ForeignKey(
        Product, related_name="purchases", on_delete=models.CASCADE
    )
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)


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
