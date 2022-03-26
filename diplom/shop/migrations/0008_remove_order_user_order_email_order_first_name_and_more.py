# Generated by Django 4.0.1 on 2022-03-26 06:20

from django.db import migrations, models
import shop.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default=2, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', validators=[shop.validators.image_resolution_check_big]),
        ),
    ]
