from django.conf import settings
from django.db import models


class Product(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(decimal_places=3, max_digits=20, default=0)


class Buy(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="purchases", on_delete=models.CASCADE
    )
    purchase = models.ForeignKey(
        Product, related_name="purchases", on_delete=models.CASCADE
    )
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)



