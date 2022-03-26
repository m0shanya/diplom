# Generated by Django 4.0.1 on 2022-03-25 07:12

from django.db import migrations, models
import shop.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_product_big_image_product_cart_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='big_image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='cart_image',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', validators=[shop.validators.image_resolution_check_big]),
        ),
    ]
