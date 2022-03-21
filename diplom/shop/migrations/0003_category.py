# Generated by Django 4.0.1 on 2022-03-14 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('choice', models.CharField(choices=[('test_1', 'Test 1'), ('test_2', 'Test 2')], max_length=100)),
                ('prod', models.ManyToManyField(to='shop.Product')),
            ],
        ),
    ]
